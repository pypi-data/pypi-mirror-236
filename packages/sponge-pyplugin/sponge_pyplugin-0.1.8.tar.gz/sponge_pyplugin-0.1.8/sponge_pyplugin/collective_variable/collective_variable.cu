#include "collective_variable.cuh"
#define CV_ERROR_CHAR_LENGTH_MAX 600

CV_MAP_TYPE* CV_MAP = new CV_MAP_TYPE;
CV_INSTANCE_TYPE* CV_INSTANCE_MAP = new CV_INSTANCE_TYPE;

void COLLECTIVE_VARIABLE_CONTROLLER::Initial(CONTROLLER* controller, int* no_direct_interaction_virtual_atom_numbers)
{
    controller->printf("START INITIALIZING CV CONTROLLER:\n");
    strcpy(module_name, "cv_controller");
    this->controller = controller;
    mdinfo = controller->mdinfo;
    if (controller->Command_Exist("cv_in_file"))
    {
		int CV_numbers = 0;
        Commands_From_In_File(controller);
		int cv_vatom_count = 0;
		for (StringMap::iterator iter = this->commands.begin(); iter != this->commands.end(); iter++)
		{
			int i = iter->first.rfind("vatom_type");
			if (i > 0 && i == (iter->first.length() - 10))
			{
				cv_vatom_name[iter->first.substr(0, i - 1)] = cv_vatom_count;
				cv_vatom_count += 1;
				no_direct_interaction_virtual_atom_numbers[0]++;
			}
			i = iter->first.rfind("CV_type");
			if (i > 0 && i == (iter->first.length() - 7))
			{
				CV_numbers++;
			}
		}
		printf("    %d CV defined\n", CV_numbers);
		printf("    %d cv virtual atoms\n", no_direct_interaction_virtual_atom_numbers[0]);
        is_initialized = 1;
		controller->printf("END INITIALIZING CV CONTROLLER\n\n");
    }
	else
	{
		controller->printf("CV CONTROLLER IS NOT INITIALIZING\n\n");
	}
    
}

static int read_one_line(FILE* In_File, char* line, char* ender)
{
    int line_count = 0;
    int ender_count = 0;
    char c;
    while ((c = getc(In_File)) != EOF)
    {
        if (line_count == 0 && (c == '\t' || c == ' '))
        {
            continue;
        }
        else if (c != '\n' && c != ',' && c != '{' && c != '}' && c != '\r')
        {
            line[line_count] = c;
            line_count += 1;
        }
        else
        {
            ender[ender_count] = c;
            ender_count += 1;
            break;
        }
    }
    while ((c = getc(In_File)) != EOF)
    {
        if (c == ' ' || c == '\t')
        {
            continue;
        }
        else if (c != '\n' && c != ',' && c != '{' && c != '}' && c != '\r')
        {
            fseek(In_File, -1, SEEK_CUR);
            break;
        }
        else
        {
            ender[ender_count] = c;
            ender_count += 1;
        }
    }
    line[line_count] = 0;
    ender[ender_count] = 0;
    if (line_count == 0 && ender_count == 0)
    {
        return EOF;
    }
    return 1;
}

void COLLECTIVE_VARIABLE_CONTROLLER::Commands_From_In_File(CONTROLLER* controller)
{
    FILE* In_File = NULL;
    if (controller->Command_Exist("cv_in_file"))
    {
        Open_File_Safely(&In_File, controller->Command("cv_in_file"), "r");
    } 
    if (In_File != NULL)
    {
        char line[CHAR_LENGTH_MAX];
        char prefix[CHAR_LENGTH_MAX] = { 0 };
        char ender[CHAR_LENGTH_MAX];
        while (true)
        {
            if (read_one_line(In_File, line, ender) == EOF)
            {
                break;
            }
            if (line[0] == '#')
            {
                if (line[1] == '#')
                {
                    if (strchr(ender, '{') != NULL)
                    {
                        int scanf_ret = sscanf(line, "%s", prefix);
                    }
                    if (strchr(ender, '}') != NULL)
                    {
                        prefix[0] = 0;
                    }
                }
                if (strchr(ender, '\n') == NULL)
                {
                    int scanf_ret = fscanf(In_File, "%*[^\n]%*[\n]");
                    fseek(In_File, -1, SEEK_CUR);
                }
            }
            else if (strchr(ender, '{') != NULL)
            {
                int scanf_ret = sscanf(line, "%s", prefix);
            }
            else
            {
                Get_Command(line, prefix);
                line[0] = 0;
            }
            if (strchr(ender, '}') != NULL)
            {
                prefix[0] = 0;
            }
        }
    }
}

void COLLECTIVE_VARIABLE_CONTROLLER::Input_Check()
{
	for (int i = 0; i < print_cv_list.size(); i++)
	{
		controller->Step_Print_Initial(print_cv_list[i]->module_name, "%.4f");
	}
    if (!(Command_Exist("dont_check_input") && atoi(Command("dont_check_input"))))
    {
        int no_warning = 0;
        for (CheckMap::iterator iter = command_check.begin(); iter != command_check.end(); iter++)
        {
            if (iter->second == 1)
            {
                printf("Warning: CV command '%s' is set, but never used.\n", iter->first.c_str());
                no_warning += 1;
            }
        }
        for (CheckMap::iterator iter = choice_check.begin(); iter != choice_check.end(); iter++)
        {
            if (iter->second == 2)
            {
                printf("Warning: the value '%s' of CV command '%s' matches none of the choices.\n", this->commands[iter->first].c_str(), iter->first.c_str());
                no_warning += 1;
            }
            else if (iter->second == 3)
            {
                printf("Warning: CV command '%s' is not set.\n", iter->first.c_str());
                no_warning += 1;
            }
        }
        if (no_warning)
        {
            printf("\nWarning: CV inputs raised %d warning(s). If You know WHAT YOU ARE DOING, press any key to continue. Set dont_check_input = 1 to disable this warning.\n", no_warning);
            getchar();
        }
    }
}

void COLLECTIVE_VARIABLE_CONTROLLER::Print_Initial()
{
    if (!is_initialized)
        return;
    controller->printf("START INITIALIZING CV PRINTER:\n");
	print_cv_list = Ask_For_CV("print", 0);
	for (int i = 0; i < print_cv_list.size(); i++)
	{
		if (controller->outputs_content.count(print_cv_list[i]->module_name))
		{
			std::string error_reason = "Reason:\n\tthe name of the CV '";
			error_reason += print_cv_list[i]->module_name;
			error_reason += "' to print is the same with a built-in output\n";
			controller->Throw_SPONGE_Error(spongeErrorConflictingCommand, "COLLECTIVE_VARIABLE_CONTROLLER::Print_Initial", error_reason.c_str());
		}
	}
    controller->printf("END INITIALIZING CV PRINTER\n\n");
}

void COLLECTIVE_VARIABLE_CONTROLLER::Step_Print(int step, int atom_numbers, UNSIGNED_INT_VECTOR* uint_crd, VECTOR scaler, VECTOR* crd, VECTOR box_length)
{
	for (int i = 0; i < print_cv_list.size(); i++)
	{
		print_cv_list[i]->Compute(atom_numbers, uint_crd, scaler, crd, box_length, CV_NEED_CPU_VALUE, step + 1);
	}
	for (int i = 0; i < print_cv_list.size(); i++)
	{
		cudaStreamSynchronize(print_cv_list[i]->cuda_stream);
		controller->Step_Print(print_cv_list[i]->module_name, print_cv_list[i]->value); 
	}
	
}

COLLECTIVE_VARIABLE_PROTOTYPE* COLLECTIVE_VARIABLE_CONTROLLER::get_CV(const char* cv_name)
{
    if (!is_initialized)
    {
		this->Throw_SPONGE_Error(spongeErrorMissingCommand, "COLLECTIVE_VARIABLE_CONTROLLER::get_CV", "Reason:\n\tcommand 'cv_in_file' is not set\n");
    }
    if (CV_INSTANCE_MAP->count(cv_name))
    {
        return CV_INSTANCE_MAP[0][cv_name];
    }
    if (Command_Exist(cv_name, "CV_type"))
    {
        char cv_type[CHAR_LENGTH_MAX];
        strcpy(cv_type, Command(cv_name, "CV_type"));
        if (CV_MAP->count(cv_type))
        {
            COLLECTIVE_VARIABLE_PROTOTYPE *cv = CV_MAP[0][cv_type](this, cv_name);
            CV_INSTANCE_MAP[0][cv_name] = cv;
            return CV_INSTANCE_MAP[0][cv_name];
        }
        else
        {
			char error_reason[CV_ERROR_CHAR_LENGTH_MAX];
			sprintf(error_reason, "Reason:\n\tthe type '%s' of the CV '%s' is undefined\n", cv_type, cv_name);
			this->Throw_SPONGE_Error(spongeErrorTypeErrorCommand, "COLLECTIVE_VARIABLE_CONTROLLER::get_CV", error_reason);
        }
        
    }
    else
    {
		char error_reason[CV_ERROR_CHAR_LENGTH_MAX];
		sprintf(error_reason, "Reason:\n\tthe type of the CV '%s' is undefined\n", cv_name);
		this->Throw_SPONGE_Error(spongeErrorTypeErrorCommand, "COLLECTIVE_VARIABLE_CONTROLLER::get_CV", error_reason);
    }
    return 0;
}

CV_LIST COLLECTIVE_VARIABLE_CONTROLLER::Ask_For_CV(const char* name, int N, float verbose_level, int layout)
{
    CV_LIST cv_list;
    int CV_numbers = 0;
    char command[CHAR_LENGTH_MAX];
	sprintf(command, "%s_CV", name);
	if (Command_Exist(command))
	{
		strcpy(command, Original_Command(command));
		char *cv_name = strtok(command, " ");
		while (cv_name != NULL)
		{
			CV_numbers += 1;
			cv_name = strtok(NULL, " ");
		}
	}
	if (N > 0 && CV_numbers != N)
	{
		char error_reason[CV_ERROR_CHAR_LENGTH_MAX];
		sprintf(error_reason, "Reason:\n\t%d CV(s) should be given to %s, but %d found\n", N, name, CV_numbers);
		Throw_SPONGE_Error(spongeErrorValueErrorCommand, "COLLECTIVE_VARIABLE_CONTROLLER::Ask_For_CV", error_reason);
	}
	else if (N <= 0 && CV_numbers < -N)
	{
		char error_reason[CV_ERROR_CHAR_LENGTH_MAX];
		sprintf(error_reason, "Reason:\n\tat least %d CV(s) should be given to %s, but only %d found\n", N, name, CV_numbers);
		Throw_SPONGE_Error(spongeErrorValueErrorCommand, "COLLECTIVE_VARIABLE_CONTROLLER::Ask_For_CV", error_reason);
	}
	if (verbose_level > -2)
	{
		for (int i = 0; i < layout; i++)
		{
			printf("    ");
		}
		printf("%d CV(s) found for %s\n", CV_numbers, name);
	}
	sprintf(command, "%s_CV", name);
	//c的strtok在此处线程不安全，只能用C++的函数分割字符串
	COLLECTIVE_VARIABLE_PROTOTYPE *cv;
	std::string value = Original_Command(command);
	auto start = value.find_first_not_of(' ', 0);
	auto stop = value.find_first_of(' ', start);
    for (int i = 0; i < CV_numbers; i++)
    {
		strcpy(command, value.substr(start, stop - start).c_str());
		if (verbose_level > -1)
		{
			for (int ii = 0; ii < layout; ii++)
			{
				printf("    ");
			}
			printf("    CV %d: %s\n", i, command);
		}
			
		cv = get_CV(command);
		if (verbose_level > -1)
		{
			for (int ii = 0; ii < layout; ii++)
			{
				printf("    ");
			}
			printf("        type of '%s' is '%s'\n", command, cv->type_name);
		}
		cv_list.push_back(cv);
		start = value.find_first_not_of(" ", stop);
		stop = value.find_first_of(" ", start);
    }
    return cv_list;
}

int* COLLECTIVE_VARIABLE_CONTROLLER::Ask_For_Int_Parameter(const char* name, const char* parameter_name, int N, int layout,
	bool raise_error_when_missing, int default_value, float verbose_level, const char* unit)
{
	if (unit == NULL)
	{
		unit = "";
	}
	int* t;
	char command[CHAR_LENGTH_MAX];
	sprintf(command, "%s_%s", name, parameter_name);
	if (!this->Command_Exist(command))
	{
		if (raise_error_when_missing)
		{
			char error_reason[CV_ERROR_CHAR_LENGTH_MAX];
			sprintf(error_reason, "Reason:\n\tno parameter %s found for %s\n", parameter_name, name);
			Throw_SPONGE_Error(spongeErrorMissingCommand, "COLLECTIVE_VARIABLE_CONTROLLER::Ask_For_Int_Parameter", error_reason);
		}
		else
		{
			strcpy(command, "");
		}
	}
	else
	{
		strcpy(command, this->Original_Command(command));
	}
	if (verbose_level > -2)
	{
		for (int _lay = 0; _lay < layout; _lay++)
			this->printf("    ");
		this->printf("reading %d %s(s) for %s\n", N, parameter_name, name);
	}
	Malloc_Safely((void**)&t, sizeof(int)* N);
	char *token = strtok(command, " ");
	for (int i = 0; i < N; i++)
	{
		if (token == NULL)
		{
			if (raise_error_when_missing)
			{
				char error_reason[CV_ERROR_CHAR_LENGTH_MAX];
				sprintf(error_reason, "Reason:\n\tthe number of parameter should be %d, but %d found\n", N, i);
				this->Throw_SPONGE_Error(spongeErrorValueErrorCommand, "COLLECTIVE_VARIABLE_CONTROLLER::Ask_For_Int_Parameter", error_reason);
			}
			else
			{
				t[i] = default_value;
				if (verbose_level > -1)
				{
					for (int _lay = 0; _lay < layout; _lay++)
						this->printf("    ");
					this->printf("    %s %d: %d %s (from default value)\n", parameter_name, i, t[i], unit);
				}

			}
		}
		else
		{
			if (cv_vatom_name.count(token))
			{
				t[i] = cv_vatom_name[token] + atom_numbers;
			}
			else if (controller->Command_Exist(token))
			{
				controller->Check_Int(token, "COLLECTIVE_VARIABLE_CONTROLLER::Ask_For_Int_Parameter");
				t[i] = atoi(controller->Command(token));
			}
			else
			{
				if (!is_str_int(token))
				{
					char error_reason[CV_ERROR_CHAR_LENGTH_MAX];
					sprintf(error_reason, "Reason:\n\t the %d-th value '%s' of the command '%s' is not an int\n", i, token, command);
					controller->Throw_SPONGE_Error(spongeErrorTypeErrorCommand, "COLLECTIVE_VARIABLE_CONTROLLER::Ask_For_Int_Parameter", error_reason);
				}
				t[i] = atoi(token);
			}
			if (verbose_level > -1)
			{
				for (int _lay = 0; _lay < layout; _lay++)
					this->printf("    ");
				this->printf("    %s %d: %d %s\n", parameter_name, i, t[i], unit);
			}
		}
		token = strtok(NULL, " ");
	}
	return t;
}

float* COLLECTIVE_VARIABLE_CONTROLLER::Ask_For_Float_Parameter(const char* name, const char* parameter_name, int N, int layout,
    bool raise_error_when_missing, float default_value, float verbose_level, const char* unit)
{
	if (unit == NULL)
	{
		unit = "";
	}
	float* t;
	char command[CHAR_LENGTH_MAX];
	sprintf(command, "%s_%s", name, parameter_name);
	if (!this->Command_Exist(command))
	{
		if (raise_error_when_missing)
		{
			char error_reason[CV_ERROR_CHAR_LENGTH_MAX];
			sprintf(error_reason, "Reason:\n\tno parameter %s found for %s\n", parameter_name, name);
			Throw_SPONGE_Error(spongeErrorMissingCommand, "COLLECTIVE_VARIABLE_CONTROLLER::Ask_For_Float_Parameter", error_reason);
		}
		else
		{
			strcpy(command, "");
		}
	}
	else
	{
		strcpy(command, this->Original_Command(command));
	}
	if (verbose_level > -2)
	{
		for (int _lay = 0; _lay < layout; _lay++)
			this->printf("    ");
		this->printf("reading %d %s(s) for %s\n", N, parameter_name, name);
	}
	Malloc_Safely((void**)&t, sizeof(float)* N);
	char *token = strtok(command, " ");
	for (int i = 0; i < N; i++)
	{
		if (token == NULL)
		{
			if (raise_error_when_missing)
			{
				char error_reason[CV_ERROR_CHAR_LENGTH_MAX];
				sprintf(error_reason, "Reason:\n\tthe number of parameter should be %d, but %d found\n", N, i);
				Throw_SPONGE_Error(spongeErrorValueErrorCommand, "COLLECTIVE_VARIABLE_CONTROLLER::Ask_For_Float_Parameter", error_reason);
			}
			else
			{
				t[i] = default_value;
				if (verbose_level > -1)
				{
					for (int _lay = 0; _lay < layout; _lay++)
						this->printf("    ");
					this->printf("    %s %d: %d %s (from default value)\n", parameter_name, i, t[i], unit);
				}

			}
		}
		else
		{
			if (controller->Command_Exist(token))
			{
				controller->Check_Float(token, "COLLECTIVE_VARIABLE_CONTROLLER::Ask_For_Float_Parameter");
				t[i] = atof(controller->Command(token));
			}
			else
			{
				if (!is_str_float(token))
				{
					char error_reason[CV_ERROR_CHAR_LENGTH_MAX];
					sprintf(error_reason, "Reason:\n\t the %d-th value '%s' of the command '%s' is not a float\n", i, token, command);
					controller->Throw_SPONGE_Error(spongeErrorTypeErrorCommand, "COLLECTIVE_VARIABLE_CONTROLLER::Ask_For_Float_Parameter", error_reason);
				}
				t[i] = atof(token);
			}
			if (verbose_level > -1)
			{
				for (int _lay = 0; _lay < layout; _lay++)
					this->printf("    ");
				this->printf("    %s %d: %f %s\n", parameter_name, i, t[i], unit);
			}
		}
		token = strtok(NULL, " ");
	}
	return t;
}

std::vector<std::string> COLLECTIVE_VARIABLE_CONTROLLER::Ask_For_String_Parameter(const char* name, const char* parameter_name, int N, int layout,
	bool raise_error_when_missing, const char* default_value, float verbose_level, const char* unit)
{
	if (unit == NULL)
	{
		unit = "";
	}
	std::vector<std::string> t;
	char command[CHAR_LENGTH_MAX];
	sprintf(command, "%s_%s", name, parameter_name);
	if (!this->Command_Exist(command))
	{
		if (raise_error_when_missing)
		{
			char error_reason[CHAR_LENGTH_MAX];
			sprintf(error_reason, "Reason:\n\tno parameter %s found for %s\n", parameter_name, name);
			Throw_SPONGE_Error(spongeErrorMissingCommand, "COLLECTIVE_VARIABLE_CONTROLLER::Ask_For_String_Parameter", error_reason);
		}
		else
		{
			strcpy(command, "");
		}
	}
	else
	{
		strcpy(command, this->Original_Command(command));
	}
	if (verbose_level > -2)
	{
		for (int _lay = 0; _lay < layout; _lay++)
			this->printf("    ");
		this->printf("reading %d %s(s) for %s\n", N, parameter_name, name);
	}
	char* token = strtok(command, " ");
	for (int i = 0; i < N; i++)
	{
		if (token == NULL)
		{
			if (raise_error_when_missing)
			{
				char error_reason[CHAR_LENGTH_MAX];
				sprintf(error_reason, "Reason:\n\tthe number of parameter should be %d, but %d found\n", N, i);
				Throw_SPONGE_Error(spongeErrorValueErrorCommand, "COLLECTIVE_VARIABLE_CONTROLLER::Ask_For_String_Parameter", error_reason);
			}
			else
			{
				t.push_back(std::string(default_value));
				if (verbose_level > -1)
				{
					for (int _lay = 0; _lay < layout; _lay++)
						this->printf("    ");
					this->printf("    %s %d: %s %s (from default value)\n", parameter_name, i, t[i].c_str(), unit);
				}

			}
		}
		else
		{
			if (controller->Command_Exist(token))
			{
				t.push_back(std::string(controller->Command(token)));
			}
			else
			{
				t.push_back(std::string(token));
			}
			if (verbose_level > -1)
			{
				for (int _lay = 0; _lay < layout; _lay++)
					this->printf("    ");
				this->printf("    %s %d: %s %s\n", parameter_name, i, t[i].c_str(), unit);
			}
		}
		token = strtok(NULL, " ");
	}
	return t;
}

std::vector<int> COLLECTIVE_VARIABLE_CONTROLLER::Ask_For_Indefinite_Length_Int_Parameter(const char* name, const char* parameter_name)
{
	std::vector<int> ints;
	char out[CHAR_LENGTH_MAX];
	std::string file_name = parameter_name;
	file_name += "_in_file";
	if (Command_Exist(name, parameter_name))
	{
		std::string strs = Original_Command(name, parameter_name);
		std::istringstream ss(strs);
		while (ss >> out)
		{
			if (cv_vatom_name.count(out))
			{
				ints.push_back(cv_vatom_name[out] + atom_numbers);
			}
			else if (controller->Command_Exist(out))
			{
				controller->Check_Int(out, "COLLECTIVE_VARIABLE_CONTROLLER::Ask_For_Indefinite_Length_Int_Parameter");
				ints.push_back(atoi(controller->Command(out)));
			}
			else
			{
				if (!is_str_int(out))
				{
					Throw_SPONGE_Error(spongeErrorTypeErrorCommand, "COLLECTIVE_VARIABLE_CONTROLLER::Ask_For_Indefinite_Length_Int_Parameter",
						"Reason:\n\tone of the value is not an int\n");
				}
				ints.push_back(atoi(out));
			}
		}
	}
	else if (Command_Exist(name, file_name.c_str()))
	{
		std::ifstream ss(Command(name, file_name.c_str()));
		while (ss >> out)
		{
			if (cv_vatom_name.count(out))
			{
				ints.push_back(cv_vatom_name[out] + atom_numbers);
			}
			else if (controller->Command_Exist(out))
			{
				controller->Check_Int(out, "COLLECTIVE_VARIABLE_CONTROLLER::Ask_For_Indefinite_Length_Int_Parameter");
				ints.push_back(atoi(controller->Command(out)));
			}
			else
			{
				if (!is_str_int(out))
				{
					Throw_SPONGE_Error(spongeErrorTypeErrorCommand, "COLLECTIVE_VARIABLE_CONTROLLER::Ask_For_Indefinite_Length_Int_Parameter",
						"Reason:\n\tone of the value is not an int\n");
				}
				ints.push_back(atoi(out));
			}
		}
	}
	return ints;
}

std::vector<float> COLLECTIVE_VARIABLE_CONTROLLER::Ask_For_Indefinite_Length_Float_Parameter(const char* name, const char* parameter_name)
{
	std::vector<float> floats;
	char out[CHAR_LENGTH_MAX];
	std::string file_name = parameter_name;
	file_name += "_in_file";
	std::string error_reason = "Reason:\n\tone value of the parameter '";
	error_reason += parameter_name;
	error_reason += "' is not a float";
	if (Command_Exist(name, parameter_name))
	{
		std::string strs = Original_Command(name, parameter_name);
		std::istringstream ss(strs);
		while (ss >> out)
		{
			if (controller->Command_Exist(out))
			{
				controller->Check_Float(out, "COLLECTIVE_VARIABLE_CONTROLLER::Ask_For_Indefinite_Length_Int_Parameter");
				floats.push_back(atof(controller->Command(out)));
			}
			else
			{
				if (!is_str_float(out))
				{
					Throw_SPONGE_Error(spongeErrorTypeErrorCommand, "COLLECTIVE_VARIABLE_CONTROLLER::Ask_For_Indefinite_Length_Int_Parameter", error_reason.c_str());
				}
				floats.push_back(atof(out));
			}
		}
	}
	else if (Command_Exist(name, file_name.c_str()))
	{
		std::ifstream ss(Command(name, file_name.c_str()));
		while (ss >> out)
		{
			if (controller->Command_Exist(out))
			{
				controller->Check_Float(out, "COLLECTIVE_VARIABLE_CONTROLLER::Ask_For_Indefinite_Length_Int_Parameter");
				floats.push_back(atof(controller->Command(out)));
			}
			else
			{
				if (!is_str_float(out))
				{
					Throw_SPONGE_Error(spongeErrorTypeErrorCommand, "COLLECTIVE_VARIABLE_CONTROLLER::Ask_For_Indefinite_Length_Int_Parameter", error_reason.c_str());
				}
				floats.push_back(atof(out));
			}
		}
	}
	return floats;
}

int COLLECTIVE_VARIABLE_PROTOTYPE::Check_Whether_Computed_At_This_Step(int step, int need)
{
    if ((need & CV_NEED_CPU_VALUE) && (last_update_step[CV_NEED_CPU_VALUE] == step))
        need &= ~CV_NEED_CPU_VALUE;
    if ((need & CV_NEED_GPU_VALUE) && (last_update_step[CV_NEED_GPU_VALUE] == step))
        need &= ~CV_NEED_GPU_VALUE;
    if ((need & CV_NEED_CRD_GRADS) && (last_update_step[CV_NEED_CRD_GRADS] == step))
        need &= ~CV_NEED_CRD_GRADS;
    if ((need & CV_NEED_BOX_GRADS) && (last_update_step[CV_NEED_BOX_GRADS] == step))
        need &= ~CV_NEED_BOX_GRADS;
    return need;
}

void COLLECTIVE_VARIABLE_PROTOTYPE::Record_Update_Step_Of_Slow_Computing_CV(int step, int need)
{
    if (need & CV_NEED_CPU_VALUE)
        last_update_step[CV_NEED_CPU_VALUE] = step;
    if (need & CV_NEED_CRD_GRADS)
        last_update_step[CV_NEED_CRD_GRADS] = step;
    if (need & CV_NEED_GPU_VALUE)
        last_update_step[CV_NEED_GPU_VALUE] = step;
    if (need & CV_NEED_BOX_GRADS)
        last_update_step[CV_NEED_BOX_GRADS] = step;
}

void COLLECTIVE_VARIABLE_PROTOTYPE::Record_Update_Step_Of_Fast_Computing_CV(int step, int need)
{
	last_update_step[CV_NEED_CRD_GRADS] = step;
	last_update_step[CV_NEED_GPU_VALUE] = step;
	last_update_step[CV_NEED_BOX_GRADS] = step;
	last_update_step[CV_NEED_CPU_VALUE] = step;
}

void COLLECTIVE_VARIABLE_PROTOTYPE::Super_Initial(COLLECTIVE_VARIABLE_CONTROLLER* manager, int atom_numbers, const char* module_name)
{
    strcpy(this->module_name, module_name);
    Cuda_Malloc_Safely((void**)&crd_grads, sizeof(VECTOR) * atom_numbers);
	Cuda_Malloc_Safely((void**)&box_grads, sizeof(VECTOR));
    Cuda_Malloc_Safely((void**)&d_value, sizeof(float));
	cudaMemset(crd_grads, 0, sizeof(VECTOR)* atom_numbers);
	cudaMemset(box_grads, 0, sizeof(VECTOR));
	cudaStreamCreate(&cuda_stream);
    last_update_step[CV_NEED_GPU_VALUE] = -1;
    last_update_step[CV_NEED_CPU_VALUE] = -1;
    last_update_step[CV_NEED_CRD_GRADS] = -1;
    last_update_step[CV_NEED_BOX_GRADS] = -1;
}

void COLLECTIVE_VARIABLE_PROTOTYPE::Initial(COLLECTIVE_VARIABLE_CONTROLLER* manager, int atom_numbers, const char* module_name)
{
	Super_Initial(manager, atom_numbers, module_name);
}
