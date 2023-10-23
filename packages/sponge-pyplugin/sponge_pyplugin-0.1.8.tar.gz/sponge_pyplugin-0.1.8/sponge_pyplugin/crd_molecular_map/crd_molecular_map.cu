#include "crd_molecular_map.cuh"

static __global__ void Calculate_No_Wrap_Crd_CUDA
(const int atom_numbers, const INT_VECTOR *box_map_times, const VECTOR box, const VECTOR *crd,
VECTOR *nowrap_crd)
{
    for (int i = threadIdx.x; i < atom_numbers; i = i + blockDim.x)
    {
        nowrap_crd[i].x = (float)box_map_times[i].int_x*box.x + crd[i].x;
        nowrap_crd[i].y = (float)box_map_times[i].int_y*box.y + crd[i].y;
        nowrap_crd[i].z = (float)box_map_times[i].int_z*box.z + crd[i].z;
    }
}

static __global__ void Refresh_BoxMapTimes_CUDA
(const int atom_numbers, const VECTOR box_length_inverse, const VECTOR *crd,
INT_VECTOR *box_map_times, VECTOR *old_crd)
{
    VECTOR crd_i, old_crd_i;
    for (int i = blockIdx.x * blockDim.x + threadIdx.x; i < atom_numbers; i += gridDim.x * blockDim.x)
    {
        crd_i = crd[i];
        old_crd_i = old_crd[i];
        box_map_times[i].int_x += floor((old_crd_i.x - crd_i.x) * box_length_inverse.x + 0.5);
        box_map_times[i].int_y += floor((old_crd_i.y - crd_i.y) * box_length_inverse.y + 0.5);
        box_map_times[i].int_z += floor((old_crd_i.z - crd_i.z) * box_length_inverse.z + 0.5);
        old_crd[i] = crd_i;
    }
}

static void Move_Crd_Nearest_From_Connectivity(CPP_ATOM_GROUP mol_atoms, VECTOR *crd, INT_VECTOR *box_map_times, const VECTOR box_length, std::vector<int> periodic_molecules)
{
    std::vector<int> atoms;
    for (int i = 0; i < mol_atoms.size(); i++)
    {
        if (periodic_molecules[i])
        {
            continue;
        }
        atoms = mol_atoms[i];
        for (int j = 1; j < atoms.size(); j++)
        {
            int atom = atoms[j];
            int atom_front = atoms[j - 1];
            int map_x = floorf((crd[atom_front].x - crd[atom].x) / box_length.x + 0.5);
            crd[atom].x = crd[atom].x + map_x * box_length.x;
            map_x = floorf((crd[atom_front].y - crd[atom].y) / box_length.y + 0.5);
            crd[atom].y = crd[atom].y + map_x * box_length.y;
            map_x = floorf((crd[atom_front].z - crd[atom].z) / box_length.z + 0.5);
            crd[atom].z = crd[atom].z + map_x * box_length.z;
        }
    }
}

static void Get_Molecule_Atoms(CONTROLLER* controller, int atom_numbers, CONECT connectivity, CPP_ATOM_GROUP &mol_atoms)
{
    //分子拓扑是一个无向图，邻接表进行描述，通过排除表形成
    int edge_numbers = 0;
    for (int i = 0; i < atom_numbers; i++)
    {
        edge_numbers += connectivity[i].size();
    }
    int* visited = NULL; //每个原子是否拜访过
    int* first_edge = NULL; //每个原子的第一个边（链表的头）
    int* edges = NULL;  //每个边的序号
    int* edge_next = NULL; //每个原子的边（链表结构）
    Malloc_Safely((void**)&visited, sizeof(int) * atom_numbers);
    Malloc_Safely((void**)&first_edge, sizeof(int) * atom_numbers);
    Malloc_Safely((void**)&edges, sizeof(int) * edge_numbers);
    Malloc_Safely((void**)&edge_next, sizeof(int) * edge_numbers);
    //初始化链表
    for (int i = 0; i < atom_numbers; i++)
    {
        visited[i] = 0;
        first_edge[i] = -1;
    }
    int atom_i, atom_j, edge_count = 0;
    for (int atom_i = 0; atom_i < atom_numbers; atom_i++)
    {
        std::set<int> conect_i = connectivity[atom_i];
        for (auto iter = conect_i.begin(); iter != conect_i.end(); iter++)
        {
            atom_j = *iter;
            edge_next[edge_count] = first_edge[atom_i];
            first_edge[atom_i] = edge_count;
            edges[edge_count] = atom_j;
            edge_count++;
        }
    }
    if (controller->Command_Exist("make_output_whole"))
    {
        char temp[CHAR_LENGTH_MAX];
        strcpy(temp, controller->Original_Command("make_output_whole"));
        char* word = strtok(temp, " -");
        while (word != NULL)
        {
            atom_i = atoi(word);
            word = strtok(NULL, "-");
            if (word == NULL)
            {
                controller->Throw_SPONGE_Error(spongeErrorValueErrorCommand, "Move_Crd_Nearest_From_Exclusions_Host",
                    "Reason:\n\t'make_output_whole' should provide atoms in the format of atom_i-atom_j");
            }
            atom_j = atoi(word);
            edge_next[edge_count] = first_edge[atom_i];
            first_edge[atom_i] = edge_count;
            edges[edge_count] = atom_j;
            edge_count++;
            edge_next[edge_count] = first_edge[atom_j];
            first_edge[atom_j] = edge_count;
            edges[edge_count] = atom_i;
            edge_count++;
            word = strtok(NULL, " ");
        }
    }
    std::deque<int> queue;
    int atom;
    for (int i = 0; i < atom_numbers; i++)
    {
        if (!visited[i])
        {
            std::vector<int> atoms;
            visited[i] = 1;
            queue.push_back(i);
            while (!queue.empty())
            {
                atom = queue[0];
                atoms.push_back(atom);
                queue.pop_front();
                edge_count = first_edge[atom];
                while (edge_count != -1)
                {
                    atom = edges[edge_count];
                    if (!visited[atom])
                    {
                        queue.push_back(atom);
                        visited[atom] = 1;
                    }
                    edge_count = edge_next[edge_count];
                }
            }
            mol_atoms.push_back(atoms);
        }
    }
    free(visited);
    free(first_edge);
    free(edges);
    free(edge_next);
}

void CoordinateMolecularMap::Record_Box_Map_Times_Host(int atom_numbers, VECTOR *crd, VECTOR *old_crd, INT_VECTOR *box_map_times, VECTOR box)
{
    for (int i = 0; i < atom_numbers; i = i + 1)
    {
        box_map_times[i].int_x += floor((old_crd[i].x - crd[i].x) / box_length.x + 0.5);
        box_map_times[i].int_y += floor((old_crd[i].y - crd[i].y) / box_length.y + 0.5);
        box_map_times[i].int_z += floor((old_crd[i].z - crd[i].z) / box_length.z + 0.5);
    }
}

std::vector<int> Check_Periodic_Molecules(CPP_ATOM_GROUP mol_atoms, const VECTOR* crd, const VECTOR box_length)
{
    std::vector<int> periodic_mols;
    std::vector<int> atoms;
    VECTOR abosolute_dr;
    for (int i = 0; i < mol_atoms.size(); i++)
    {
        atoms = mol_atoms[i];
        abosolute_dr.x = 0;
        abosolute_dr.y = 0;
        abosolute_dr.z = 0;
        for (int j = 1; j < atoms.size(); j++)
        {
            int atom = atoms[j];
            int atom_front = atoms[j-1];
            abosolute_dr = abosolute_dr + Get_Periodic_Displacement(crd[atom], crd[atom_front], box_length);
        }
        periodic_mols.push_back(abosolute_dr.x * abosolute_dr.x >= box_length.x * box_length.x
            || abosolute_dr.y * abosolute_dr.y >= box_length.y * box_length.y
            || abosolute_dr.z * abosolute_dr.z >= box_length.z * box_length.z); 
    }
    return periodic_mols;
}

void CoordinateMolecularMap::Initial(CONTROLLER *controller, int atom_numbers, VECTOR box_length, VECTOR *crd, 
    CONECT connectivity, const char *module_name)
{
    if (module_name == NULL)
    {
        strcpy(this->module_name, "crd_mole_wrap");
    }
    else
    {
        strcpy(this->module_name, module_name);
    }

    this->atom_numbers = atom_numbers;
    this->box_length = box_length;
    
    Cuda_Malloc_Safely((void**)&nowrap_crd, sizeof(VECTOR)*atom_numbers);
    Cuda_Malloc_Safely((void**)&old_crd, sizeof(VECTOR)*atom_numbers);
    Cuda_Malloc_Safely((void**)&box_map_times, sizeof(INT_VECTOR)*atom_numbers);

    Malloc_Safely((void**)&h_nowrap_crd, sizeof(VECTOR)*atom_numbers);
    Malloc_Safely((void**)&h_old_crd, sizeof(VECTOR)*atom_numbers);
    Malloc_Safely((void**)&h_box_map_times, sizeof(INT_VECTOR)*atom_numbers);
    cudaMemcpy(h_nowrap_crd, crd, sizeof(VECTOR) * atom_numbers, cudaMemcpyDeviceToHost);
    for (int i = 0; i < atom_numbers; i = i + 1)
    {
        h_old_crd[i] = h_nowrap_crd[i];
        h_box_map_times[i].int_x = 0;
        h_box_map_times[i].int_y = 0;
        h_box_map_times[i].int_z = 0;
    }
    if (controller[0].Command_Exist("molecule_map_output"))
    {
        controller->Warn("'molecule_map_output' is a deprecated command since version 1.4");
    }
    Get_Molecule_Atoms(controller, atom_numbers, connectivity, molecule_atoms);
    periodic_molecules = Check_Periodic_Molecules(molecule_atoms, h_nowrap_crd, box_length);
    Move_Crd_Nearest_From_Connectivity(molecule_atoms, h_nowrap_crd, h_box_map_times, box_length, periodic_molecules);
    //使用cuda内部函数，给出占用率最大的block和thread参数
    cudaOccupancyMaxPotentialBlockSize(&blocks_per_grid, &threads_per_block, Refresh_BoxMapTimes_CUDA, 0, 0);

    cudaMemcpy(nowrap_crd, h_nowrap_crd, sizeof(VECTOR)*atom_numbers, cudaMemcpyHostToDevice);
    cudaMemcpy(old_crd, h_old_crd, sizeof(VECTOR)*atom_numbers, cudaMemcpyHostToDevice);
    cudaMemcpy(box_map_times, h_box_map_times, sizeof(INT_VECTOR)*atom_numbers, cudaMemcpyHostToDevice);
    is_initialized = 1;
}

void CoordinateMolecularMap::Calculate_No_Wrap_Crd(const VECTOR *crd)
{
    if (is_initialized)
        Calculate_No_Wrap_Crd_CUDA << <blocks_per_grid, threads_per_block >> >(atom_numbers, box_map_times, box_length, crd, nowrap_crd);
}

void CoordinateMolecularMap::Refresh_BoxMapTimes(const VECTOR *crd)
{
    if (is_initialized)
    {
        Refresh_BoxMapTimes_CUDA << <blocks_per_grid, threads_per_block >> >
            (atom_numbers, 1.0 / box_length, crd,
            box_map_times, old_crd);
    }
}

void CoordinateMolecularMap::Update_Volume(VECTOR box_length)
{
    if (!is_initialized)
        return;
    this->box_length = box_length;
}
