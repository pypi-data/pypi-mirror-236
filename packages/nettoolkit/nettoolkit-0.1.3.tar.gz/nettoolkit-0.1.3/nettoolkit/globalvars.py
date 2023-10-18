
# ---------------------------------------------------------------------------------------
from nettoolkit.forms import btn_ipscanner_exec, btn_minitools_exec, btn_captureit_exec, btn_factsfinder_exec
#
from nettoolkit.forms.md5_calculator import md5_calculator_exec, md5_calculator_frame
from nettoolkit.forms.pw_enc_dec import pw_enc_cisco_exec, pw_dec_cisco_exec, pw_enc_juniper_exec, pw_dec_juniper_exec, pw_enc_decr_frame
from nettoolkit.forms.prefixes_oper import prefixes_oper_summary_exec, prefixes_oper_issubset_exec, prefixes_oper_pieces_exec, prefixes_oper_frame
from nettoolkit.forms.juniper_oper import juniper_oper_to_jset_exec, juniper_oper_remove_remarks_exec, juniper_oper_frame
#
from nettoolkit.forms.subnet_scanner import subnet_scanner_exec, subnet_scanner_frame
from nettoolkit.forms.compare_scanner_outputs import compare_scanner_outputs_exec, compare_scanner_outputs_frame
from nettoolkit.forms.create_batch import create_batch_exec, create_batch_frame
#
from capture_it.forms.cred import *
from capture_it.forms.options import *
from capture_it.forms.common_to_all import *
from capture_it.forms.custom import *
#
from nettoolkit.forms.ff_generate import *
from nettoolkit.forms.ff_custom import *
# ---------------------------------------------------------------------------------------

# ---------------------------------------------------------------------------------------
# GLOBAL VARS
# ---------------------------------------------------------------------------------------
MINITOOLS_FRAMES = {
	'MD5 Calculate': md5_calculator_frame(),
	'P/W Enc/Dec': pw_enc_decr_frame(),
	'Prefix Operations': prefixes_oper_frame(),
	'Juniper': juniper_oper_frame(),
}
IPSCANNER_FRAMES = {
	'Subnet Scanner': subnet_scanner_frame(),
	'Compare Scanner Outputs': compare_scanner_outputs_frame(),
	'Create Batch': create_batch_frame(),
}
CAPTUREIT_FRAMES = {
	'cred': exec_cred_frame(),
	'options': exec_options_frame(),
	'custom': exec_custom_frame(),
	'custom-facts': exec_ff_custom_frame(),
	'Common': exec_common_to_all_frame(),
}
FACTSFINDER_FRAMES = {
	'facts-finder': btn_ff_gen_frame(),	
	'custom-facts': exec_ff_custom_frame(),
}
PYVIG_FRAMES = {
	# 'Input pyVig Data': pv_input_data_frame(),   # self.input_data()
	# 'pyVig Filters': pv_apply_filters_frame(),  # self.select_filters()
	# 'pyVig Options': pv_options_frame(),   # self.other_options()
}
# --------------------------------------------------------
MINITOOLS_EVENT_FUNCS = {
	'go_md5_calculator': md5_calculator_exec,
	'go_pw_enc_cisco': pw_enc_cisco_exec,
	'go_pw_dec_cisco': pw_dec_cisco_exec,
	'go_pw_enc_juniper': pw_enc_juniper_exec,
	'go_pw_dec_juniper': pw_dec_juniper_exec,
	'go_pfxs_summary': prefixes_oper_summary_exec,
	'go_pfxs_issubset' : prefixes_oper_issubset_exec,
	'go_pfxs_break': prefixes_oper_pieces_exec,
	'go_juniper_to_set': juniper_oper_to_jset_exec,
	'go_juniper_remove_remarks': juniper_oper_remove_remarks_exec,
}
IPSCANNER_EVENT_FUNCS = {
	'btn_ipscanner': btn_ipscanner_exec,
	'go_subnet_scanner': subnet_scanner_exec,
	'go_compare_scanner_outputs': compare_scanner_outputs_exec,
	'go_create_batch': create_batch_exec,
	'btn_minitools': btn_minitools_exec,
}
CATPUREIT_EVENT_FUNCS = {
	'device_ip_list_file': device_ip_list_file_exec,
	'cisco_cmd_list_file': cisco_cmd_list_file_exec,
	'juniper_cmd_list_file': juniper_cmd_list_file_exec,
	'cit_common': cit_common_exec,
	'custom_cit_file': custom_cit_file_exec,
	'custom_dynamic_cmd_class_name': custom_dynamic_cmd_class_name_exec,
	'generate_facts': generate_facts_exec,
	'custom_ff_file': custom_ff_file_exec,
	'custom_fk_file': custom_fk_file_exec,
	'custom_ff_class_name': custom_ff_name_exec,
	'custom_fk_name': custom_fk_name_exec,
	'btn_captureit': btn_captureit_exec,
}
FACTSFINDER_EVENT_FUNCS = {
	'btn_ff_gen': btn_ff_gen_exec, 
	'btn_factsfinder': btn_factsfinder_exec,
	'custom_ff_file': custom_ff_file_exec,
	'custom_fk_file': custom_fk_file_exec,
	'custom_ff_class_name': custom_ff_name_exec,
	'custom_fk_name': custom_fk_name_exec,
}
PYVIG_EVENT_FUNCS = {
	# 'is_sheet_filter': is_sheet_filter_exec, #event_update_filter 
	# 'filt_col_add': filt_col_add_exec, # sheet_filter_add_col_value
	# 'def_stn': def_stn_exec, #update_default_stencil
	# 'enable_description_merge': enable_description_merge_exec, #update_description_col_dropbox
	# 'desc_col_add': desc_col_add_exec, # append_description_column
	# 'data_file': data_file_exec, # update_cabling_sheet_columns & update_devices_sheet_columns
	# 'btn_pv_gen': btn_pv_gen_exec,  # check_basics, and event_update_Go
}
# --------------------------------------------------------
MINITOOLS_EVENT_UPDATERS = {
	'go_md5_calculator',
	'go_pw_enc_cisco', 'go_pw_dec_cisco', 'go_pw_enc_juniper', 'go_pw_dec_juniper',
	'go_pfxs_summary', 'go_pfxs_issubset', 'go_pfxs_break',
}
IPSCANNER_EVENT_UPDATERS = set()
CAPTUREIT_EVENT_UPDATERS = {
	'cit_common',
	'device_ip_list_file', 'cisco_cmd_list_file', 'juniper_cmd_list_file',
	'custom_cit_file', 'custom_dynamic_cmd_class_name',
	'generate_facts', 'custom_ff_file', 'custom_ff_class_name', 'custom_fk_file', 'custom_fk_name',	
}

TAB_EVENT_UPDATERS = { 'btn_ipscanner', 'btn_minitools', 'btn_captureit', 'btn_factsfinder'}
FACTSFINDER_EVENT_UPDATERS = {
	'btn_ff_gen',
	'generate_facts', 'custom_ff_file', 'custom_ff_class_name', 'custom_fk_file', 'custom_fk_name',	
}
PYVIG_EVENT_UPDATERS = {
	'is_sheet_filter', 'enable_description_merge', 'desc_col_add', 
}
# --------------------------------------------------------
MINITOOLS_RETRACTABLES = {
	'file_md5_hash_check', 'file_md5_hash_value',
	'pw_result_juniper', 'pw_result_cisco', 'pw_cisco', 'pw_juniper',
	'pfxs_summary_input', 'pfxs_summary_result', 'pfxs_subnet', 'pfxs_supernet', 'pfxs_issubset_result', 
	'pfxs_subnet1', 'pfxs_pieces', 'pfxs_pieces_result',
	'file_juniper', 'op_folder_juniper',
}
IPSCANNER_RETRACTABLES = {
	'op_folder', 'pfxs', 'sockets', 'till', 
	'file1', 'file2',
	'op_folder_create_batch', 'pfxs_create_batch', 'names_create_batch', 'ips_create_batch',
}
CAPTUREIT_RETRACTABLES = {
	'cit_op_folder', 'cred_en', 'cred_un', 'cred_pw', 
	'device_ip_list_file', 'device_ips',
	'cisco_cmd_list_file', 'cisco_cmds',
	'juniper_cmd_list_file', 'juniper_cmds',
	'custom_cit_file', 'custom_dynamic_cmd_class_name', 'custom_dynamic_cmd_class_str',
	'custom_ff_file', 'custom_ff_class_name', 'custom_ff_class_str',
	'custom_fk_file', 'custom_fk_name','custom_fk_str',
	'append_to', 'common_log_file', 'cred_log_type', 'concurrent_connections', 'visual_progress',
}
FACTSFINDER_RETRACTABLES = {
	'ff_log_files', 	
	'custom_ff_file', 'custom_ff_class_name', 'custom_ff_class_str',
	'custom_fk_file', 'custom_fk_name','custom_fk_str',
}
PYVIG_RETRACTABLES = {
	
}

# --------------------------------------------------------
# ---------------------------------------------------------------------------------------
