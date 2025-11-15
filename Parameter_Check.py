import os
import cloudpss   
import time
import numpy as np
import logging
from datetime import datetime
import numpy.linalg as lg
import math

# 配置日志
def setup_logging():
    # 创建日志文件名，包含时间戳
    log_filename = f"device_changes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    # 配置日志格式
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )
    
    logging.info("=== 设备参数调整日志开始 ===")
    return log_filename

if __name__ == '__main__':
    
    # 设置日志
    log_filename = setup_logging()
    logging.info(f"日志文件已创建: {log_filename}")
    
    # token和服务器设置
    os.environ['CLOUDPSS_API_URL'] = '{server_id}'

    cloudpss.setToken('{sdk_token}')

    # 获取项目实例
    model =  cloudpss.Model.fetch('{model_id}')
    
    # 发电机电磁暂态参数检查
    #################################################################################
    ################################### 无权限公开 ##################################
    ##################################################################################
    
    # # 获取模型中所有发电机元件的实例
    comp_Gen = model.getComponentsByRid('model/CloudPSS/SyncGeneratorRouter')
    logging.info(f"开始检查发电机元件，共 {len(comp_Gen)} 个")

    Gen_adjustments = 0
    for key in comp_Gen.keys():
        comp = model.getComponentByKey(key)
        comp_name = getattr(comp, 'label', key)
        
        tmp_capacity = max( abs(float(comp.args['AP']))/0.9, (float(comp.args['AP'])**2 + float(comp.args['RP'])**2)**0.5 )

        if float(comp.args['Smva']) <  np.floor(tmp_capacity):
            if True:
                old_value = comp.args['Smva']
                comp.args['Smva'] = tmp_capacity
                logging.info(f"发电机 {comp_name} 的 Smva 参数调整: {old_value} -> {tmp_capacity} (触发条件: Smva <= |AP|/0.9")
                Gen_adjustments += 1
                
        if float(comp.args['BusType']) == 1 and float(comp.args['pf_Qmin']) <= -99999:
                old_value = comp.args['pf_Qmin']
                comp.args['pf_Qmin'] = 0
                logging.info(f"发电机 {comp_name} 的 pf_Qmin 参数调整: {old_value} -> {0} (触发条件: pf_Qmin <= -99999")
                Vsource_adjustments += 1
    
    logging.info(f"发电机元件调整完成，共进行了 {Gen_adjustments} 次调整")

    # 获取模型中所有变压器元件的实例
    comp_Transformer = model.getComponentsByRid('model/CloudPSS/_newTransformer_3p2w')
    logging.info(f"开始检查变压器元件，共 {len(comp_Transformer)} 个")

    transformer_adjustments = 0
    for key in comp_Transformer.keys():
        comp = model.getComponentByKey(key)
        comp_name = getattr(comp, 'label', key)
        
        # 不自动处理
    
    logging.info(f"变压器元件调整完成，共进行了 {transformer_adjustments} 次调整")
    
    
    
    # 获取模型中所有理想电压源元件的实例
    comp_Vsource = model.getComponentsByRid('model/CloudPSS/_newACVoltageSource_3p')
    logging.info(f"开始检查理想电压源元件，共 {len(comp_Vsource)} 个")

    Vsource_adjustments = 0
    for key in comp_Vsource.keys():
        comp = model.getComponentByKey(key)
        comp_name = getattr(comp, 'label', key)

        if float(comp.args['BusType']) == '1' and float(comp.args['pf_Qmin']) <= -99999:
                old_value = comp.args['pf_Qmin']
                comp.args['pf_Qmin'] = 0
                logging.info(f"理想电压源 {comp_name} 的 pf_Qmin 参数调整: {old_value} -> {0} (触发条件: pf_Qmin <= -99999")
                Vsource_adjustments += 1

    logging.info(f"理想电压源元件调整完成，共进行了 {Vsource_adjustments} 次调整")

    # 获取模型中所有GM元件的实例
    comp_GM = model.getComponentsByRid('model/CloudPSS/_GMGoverner')
    logging.info(f"开始检查GM元件，共 {len(comp_GM)} 个")

    gm_adjustments = 0
    for key in comp_GM.keys():
        comp = model.getComponentByKey(key)
        comp_name = getattr(comp, 'label', key)
        
        # 若DBMAX2/DBMIN2/DB2/DB2_/DB1/DB1_参数超过限值，则将其统一修改为1/-1
        if float(comp.args['DBMAX2']) > 1 or float(comp.args['DBMAX2']) <0:
            old_value = comp.args['DBMAX2']
            comp.args['DBMAX2'] = str(0)
            logging.info(f"GM元件 {comp_name} 的 DBMAX2 参数调整: {old_value} -> 1 (触发条件: DBMAX2 > 1)")
            gm_adjustments += 1

        if float(comp.args['DBMIN2']) < -1 or float(comp.args['DBMIN2']) > 0:
            old_value = comp.args['DBMIN2']
            comp.args['DBMIN2'] = str(0)
            logging.info(f"GM元件 {comp_name} 的 DBMIN2 参数调整: {old_value} -> -1 (触发条件: DBMIN2 < -1)")
            gm_adjustments += 1

        if float(comp.args['DB2']) > 1 or float(comp.args['DB2']) < 0:
            old_value = comp.args['DB2']
            comp.args['DB2'] = str(0)
            logging.info(f"GM元件 {comp_name} 的 DB2 参数调整: {old_value} -> 1 (触发条件: DB2 > 1)")
            gm_adjustments += 1

        if float(comp.args['DB2_']) <- 1 or float(comp.args['DB2_']) > 0:
            old_value = comp.args['DB2_']
            comp.args['DB2_'] = str(0)
            logging.info(f"GM元件 {comp_name} 的 DB2_ 参数调整: {old_value} -> 1 (触发条件: DB2_ > 1)")
            gm_adjustments += 1

        if float(comp.args['DB1']) > 1 or float(comp.args['DB1']) < 0:
            old_value = comp.args['DB1']
            comp.args['DB1'] = str(0)
            logging.info(f"GM元件 {comp_name} 的 DB1 参数调整: {old_value} -> 1 (触发条件: DB1 > 1)")
            gm_adjustments += 1

        if float(comp.args['DB1_']) < -1 or float(comp.args['DB1_']) > 0:
            old_value = comp.args['DB1_']
            comp.args['DB1_'] = str(0)
            logging.info(f"GM元件 {comp_name} 的 DB1_ 参数调整: {old_value} -> -1 (触发条件: DB1_ < -1)")
            gm_adjustments += 1
        
        if float(comp.args['INTG_MAX']) <= 0:
            old_value = comp.args['INTG_MAX']
            comp.args['INTG_MAX'] = str(10)
            logging.info(f"GNGoverner元件 {comp_name} 的 INTG_MAX 参数调整: {old_value} -> 1 (触发条件: INTG_MAX > 1)")
            gm_adjustments += 1

        if float(comp.args['INTG_MIN']) >= 0:
            old_value = comp.args['INTG_MIN']
            comp.args['INTG_MIN'] = str(-1)
            logging.info(f"GNGoverner元件 {comp_name} 的 INTG_MIN 参数调整: {old_value} -> -1 (触发条件: INTG_MIN >= 0)")
            gm_adjustments += 1

        if float(comp.args['PID_MAX']) <= 0:
            old_value = comp.args['PID_MAX']
            comp.args['PID_MAX'] = str(10)
            logging.info(f"GNGoverner元件 {comp_name} 的 PID_MAX 参数调整: {old_value} -> 1 (触发条件: PID_MAX > 1)")
            gm_adjustments += 1

        if float(comp.args['PID_MIN']) >= 0:
            old_value = comp.args['PID_MIN']
            comp.args['PID_MIN'] = str(-1)
            logging.info(f"GNGoverner元件 {comp_name} 的 PID_MIN 参数调整: {old_value} -> -1 (触发条件: PID_MIN >= 0)")
            gm_adjustments += 1
            
        # 若Ki参数过大，则将其统一修改为0.1
        if float(comp.args['Ki']) == 0:
            old_value = comp.args['Ki']
            comp.args['Ki'] = str(0.1)
            logging.info(f"GMGoverner元件 {comp_name} 的 Ki 参数调整: {old_value} -> 0.1 (触发条件: Ki == 0)")
            gm_adjustments += 1
    
    logging.info(f"GM元件调整完成，共进行了 {gm_adjustments} 次调整")

    # 获取模型中所有负荷元件的实例
    comp_Load = model.getComponentsByRid('model/CloudPSS/_newExpLoad_3p')
    logging.info(f"开始检查负荷元件，共 {len(comp_Load)} 个")

    # 遍历每个负荷元件，利用 getComponetByKey 方法获取每个负荷元件实例
    load_adjustments = 0
    for key in comp_Load.keys():
        comp = model.getComponentByKey(key)
        comp_name = getattr(comp, 'label', key)
        
        # 若p参数超过限值，则将其统一修改为0
        if float(comp.args['p']) < 0:
            old_value = comp.args['p']
            comp.args['p'] = str(0)
            logging.info(f"负荷元件 {comp_name} 的 p 参数调整: {old_value} -> 0 (触发条件: p < 0)")
            load_adjustments += 1
    
    logging.info(f"负荷元件调整完成，共进行了 {load_adjustments} 次调整")

    # 获取模型中所有LCC元件的实例
    comp_LCC = model.getComponentsByRid('model/CloudPSS/DCLine_sp')
    logging.info(f"开始检查LCC元件，共 {len(comp_LCC)} 个")

    lcc_adjustments = 0
    for key in comp_LCC.keys():
        comp = model.getComponentByKey(key)
        comp_name = getattr(comp, 'label', key)
        
        # 若Ll参数过小，则将其统一修改为1000
        if float(comp.args['Ll']) < 1:
            old_value = comp.args['Ll']
            comp.args['Ll'] = str(1000)
            logging.info(f"LCC元件 {comp_name} 的 Ll 参数调整: {old_value} -> 1000 (触发条件: Ll < 1)")
            lcc_adjustments += 1
    
    logging.info(f"LCC元件调整完成，共进行了 {lcc_adjustments} 次调整")
            
    # 获取模型中所有E_F_MNOPQRST_Exciter元件的实例
    comp_MNOPQRST_Exciter = model.getComponentsByRid('model/CloudPSS/_F_MNOPQRST_Exciter')
    logging.info(f"开始检查E_F_MNOPQRST_Exciter元件，共 {len(comp_MNOPQRST_Exciter)} 个")
    
    mnopqrst_adjustments = 0
    for key in comp_MNOPQRST_Exciter.keys():
        comp = model.getComponentByKey(key)
        comp_name = getattr(comp, 'label', key)
        
        # 若VRMIN参数过大，则将其统一修改为-100
        if float(comp.args['VRMIN']) > 0:
            old_value = comp.args['VRMIN']
            comp.args['VRMIN'] = str(-100)
            logging.info(f"E_F_MNOPQRST_Exciter元件 {comp_name} 的 VRMIN 参数调整: {old_value} -> -100 (触发条件: VRMIN > 0)")
            mnopqrst_adjustments += 1
            
        if float(comp.args['C1']) <= 1e-5 or float(comp.args['C1']) >= 3:
            old_value = comp.args['C1']
            comp.args['C1'] = str(0.0001667956)
            comp.args['C2'] = str(1.0991057504)
            logging.info(f"E_F_MNOPQRST_Exciter元件 {comp_name} 的 C1 C2组参数调整: {old_value} -> 0.01 (触发条件: C1 <= 1e-5 或 C2 >= 3)")
            mnopqrst_adjustments += 1
            
        if float(comp.args['KC']) <= 0:
            old_value = comp.args['KC']
            comp.args['KC'] = str(0.1)
            logging.info(f"E_F_MNOPQRST_Exciter元件 {comp_name} 的 KC 参数调整: {old_value} -> 0.1 (触发条件: KC <= 0)")
            mnopqrst_adjustments += 1
            
        if float(comp.args['KD']) <= 0:
            old_value = comp.args['KD']
            comp.args['KD'] = str(0.1)
            logging.info(f"E_F_MNOPQRST_Exciter元件 {comp_name} 的 KD 参数调整: {old_value} -> 0.1 (触发条件: KD <= 0)")
            mnopqrst_adjustments += 1
    
    logging.info(f"E_F_MNOPQRST_Exciter元件调整完成，共进行了 {mnopqrst_adjustments} 次调整")
            
    # 获取模型中所有UV_Exciter元件的实例
    comp_UV_Exciter = model.getComponentsByRid('model/CloudPSS/_F_UV_Exciter')
    logging.info(f"开始检查UV_Exciter元件，共 {len(comp_UV_Exciter)} 个")
    
    uv_adjustments = 0
    for key in comp_UV_Exciter.keys():
        comp = model.getComponentByKey(key)
        comp_name = getattr(comp, 'label', key)
        
        # 若VRMIN参数过大，则将其统一修改为-100
        if float(comp.args['VRMIN']) > 0:
            old_value = comp.args['VRMIN']
            comp.args['VRMIN'] = str(-100)
            logging.info(f"UV_Exciter元件 {comp_name} 的 VRMIN 参数调整: {old_value} -> -100 (触发条件: VRMIN > 0)")
            uv_adjustments += 1
    
    logging.info(f"UV_Exciter元件调整完成，共进行了 {uv_adjustments} 次调整")
    
    # 获取模型中所有GAGoverner元件的实例
    comp_GAGoverner = model.getComponentsByRid('model/CloudPSS/_GAGoverner')
    logging.info(f"开始检查GAGoverner元件，共 {len(comp_GAGoverner)} 个")
    
    ga_adjustments = 0
    for key in comp_GAGoverner.keys():
        comp = model.getComponentByKey(key)
        comp_name = getattr(comp, 'label', key)
        
        # 若PGV_DELAY参数过大，则将其统一修改为0.95
        if float(comp.args['PGV_DELAY']) > 0.95:
            old_value = comp.args['PGV_DELAY']
            comp.args['PGV_DELAY'] = str(0.95)
            logging.info(f"GAGoverner元件 {comp_name} 的 PGV_DELAY 参数调整: {old_value} -> 0.95 (触发条件: PGV_DELAY > 0.95)")
            ga_adjustments += 1
            
        if float(comp.args['Ki']) <= 0:
            old_value = comp.args['Ki']
            comp.args['Ki'] = str(0.1)
            logging.info(f"GAGoverner元件 {comp_name} 的 Ki 参数调整: {old_value} -> 0.1 (触发条件: Ki <= 0)")
            ga_adjustments += 1

        if float(comp.args['INTG_MAX']) <= 0:
            old_value = comp.args['INTG_MAX']
            comp.args['INTG_MAX'] = str(10)
            logging.info(f"GAGoverner元件 {comp_name} 的 INTG_MAX 参数调整: {old_value} -> 1 (触发条件: INTG_MAX > 1)")
            ga_adjustments += 1

        if float(comp.args['INTG_MIN']) >= 0:
            old_value = comp.args['INTG_MIN']
            comp.args['INTG_MIN'] = str(-1)
            logging.info(f"GAGoverner元件 {comp_name} 的 INTG_MIN 参数调整: {old_value} -> -1 (触发条件: INTG_MIN >= 0)")
            ga_adjustments += 1

        if float(comp.args['PID_MAX']) <= 0:
            old_value = comp.args['PID_MAX']
            comp.args['PID_MAX'] = str(10)
            logging.info(f"GAGoverner元件 {comp_name} 的 PID_MAX 参数调整: {old_value} -> 1 (触发条件: PID_MAX > 1)")
            ga_adjustments += 1

        if float(comp.args['PID_MIN']) >= 0:
            old_value = comp.args['PID_MIN']
            comp.args['PID_MIN'] = str(-1)
            logging.info(f"GAGoverner元件 {comp_name} 的 PID_MIN 参数调整: {old_value} -> -1 (触发条件: PID_MIN >= 0)")
            ga_adjustments += 1
            
        if float(comp.args['VELclose']) >= 0:
            old_value = comp.args['VELclose']
            comp.args['VELclose'] = str(-0.1)
            logging.info(f"GAGoverner元件 {comp_name} 的 PID_MIN 参数调整: {old_value} -> -0.1 (触发条件: VELclose >= 0)")
            ga_adjustments += 1
        
    
    logging.info(f"GAGoverner元件调整完成，共进行了 {ga_adjustments} 次调整")
            
    # 获取模型中所有GIGoverner元件的实例
    comp_GIGoverner = model.getComponentsByRid('model/CloudPSS/_GIGoverner')
    logging.info(f"开始检查GIGoverner元件，共 {len(comp_GIGoverner)} 个")
    
    gi_adjustments = 0
    for key in comp_GIGoverner.keys():
        comp = model.getComponentByKey(key)
        comp_name = getattr(comp, 'label', key)
        
        # 若Ki参数过大，则将其统一修改为0.1
        if float(comp.args['Ki1']) == 0:
            old_value = comp.args['Ki1']
            comp.args['Ki1'] = str(0.1)
            logging.info(f"GIGoverner元件 {comp_name} 的 Ki1 参数调整: {old_value} -> 0.1 (触发条件: Ki1 == 0)")
            gi_adjustments += 1
            
        if float(comp.args['Ki2']) <= 0:
            old_value = comp.args['Ki2']
            comp.args['Ki2'] = str(0.1)
            logging.info(f"GIGoverner元件 {comp_name} 的 Ki2 参数调整: {old_value} -> 0.1 (触发条件: Ki2 == 0)")
            gi_adjustments += 1
            
        if float(comp.args['INTG_MAX1']) <= 0:
            old_value = comp.args['INTG_MAX1']
            comp.args['INTG_MAX1'] = str(1)
            logging.info(f"GIGoverner元件 {comp_name} 的 INTG_MAX1 参数调整: {old_value} -> 1 (触发条件: INTG_MAX1 == 0)")
            gi_adjustments += 1
            
        if float(comp.args['INTG_MIN1']) >= 0:
            old_value = comp.args['INTG_MIN1']
            comp.args['INTG_MIN1'] = str(-1)
            logging.info(f"GIGoverner元件 {comp_name} 的 INTG_MIN1 参数调整: {old_value} -> - (触发条件: INTG_MIN1 == 0)")
            gi_adjustments += 1
            
        if float(comp.args['PID_MAX1']) <= 0:
            old_value = comp.args['PID_MAX1']
            comp.args['PID_MAX1'] = str(1)
            logging.info(f"GIGoverner元件 {comp_name} 的 PID_MAX1 参数调整: {old_value} -> 1 (触发条件: PID_MAX1 == 0)")
            gi_adjustments += 1
            
        if float(comp.args['PID_MIN1']) >= 0:
            old_value = comp.args['PID_MIN1']
            comp.args['PID_MIN1'] = str(-1)
            logging.info(f"GIGoverner元件 {comp_name} 的 PID_MIN1 参数调整: {old_value} -> - (触发条件: PID_MIN1 == 0)")
            gi_adjustments += 1
            
        if float(comp.args['INTG_MAX2']) <= 0:
            old_value = comp.args['INTG_MAX2']
            comp.args['INTG_MAX2'] = str(1)
            logging.info(f"GIGoverner元件 {comp_name} 的 INTG_MAX2 参数调整: {old_value} -> 1 (触发条件: INTG_MAX2 == 0)")
            gi_adjustments += 1
            
        if float(comp.args['INTG_MIN2']) >= 0:
            old_value = comp.args['INTG_MIN2']
            comp.args['INTG_MIN2'] = str(-1)
            logging.info(f"GIGoverner元件 {comp_name} 的 INTG_MIN2 参数调整: {old_value} -> - (触发条件: INTG_MIN2 == 0)")
            gi_adjustments += 1
            
        if float(comp.args['PID_MAX2']) <= 0:
            old_value = comp.args['PID_MAX2']
            comp.args['PID_MAX2'] = str(1)
            logging.info(f"GIGoverner元件 {comp_name} 的 PID_MAX2 参数调整: {old_value} -> 1 (触发条件: PID_MAX2 == 0)")
            gi_adjustments += 1
            
        if float(comp.args['PID_MIN2']) >= 0:
            old_value = comp.args['PID_MIN2']
            comp.args['PID_MIN2'] = str(-1)
            logging.info(f"GIGoverner元件 {comp_name} 的 PID_MIN2 参数调整: {old_value} -> 1 (触发条件: PID_MIN2 == 0)")
            gi_adjustments += 1
            
        if float(comp.args['CON_MAX']) <= 0:
            old_value = comp.args['CON_MAX']
            comp.args['CON_MAX'] = str(1)
            logging.info(f"GIGoverner元件 {comp_name} 的 CON_MAX 参数调整: {old_value} -> - (触发条件: CON_MAX == 0)")
            gi_adjustments += 1
            
        if float(comp.args['CON_MIN']) >= 0:
            old_value = comp.args['CON_MIN']
            comp.args['CON_MIN'] = str(-1)
            logging.info(f"GIGoverner元件 {comp_name} 的 CON_MIN 参数调整: {old_value} -> - (触发条件: CON_MIN == 0)")
            gi_adjustments += 1
    
    logging.info(f"GIGoverner元件调整完成，共进行了 {gi_adjustments} 次调整")
    
    
    comp_GHGoverner = model.getComponentsByRid('model/CloudPSS/_GHGoverner')
    logging.info(f"开始检查GHGoverner元件，共 {len(comp_GHGoverner)} 个")
    
    gh_gov_adjustments = 0
    for key in comp_GHGoverner.keys():
        comp = model.getComponentByKey(key)
        comp_name = getattr(comp, 'label', key)
        
        # 若Ki参数过大，则将其统一修改为0.1
        if float(comp.args['PMAX']) <= 0:
            old_value = comp.args['PMAX']
            comp.args['PMAX'] = str(float(comp.args['Sb']) * 0.90)
            logging.info(f"GHGoverner元件 {comp_name} 的 PMAX 参数调整: {old_value} -> Sbase (触发条件: PMAX <= 0)")
            gh_gov_adjustments += 1
            
    logging.info(f"GHGoverner元件调整完成，共进行了 {gh_gov_adjustments} 次调整")
    
            
    # 获取模型中所有GJGoverner元件的实例
    comp_GJGoverner = model.getComponentsByRid('model/CloudPSS/_GJGoverner')
    logging.info(f"开始检查GJGoverner元件，共 {len(comp_GJGoverner)} 个")
    
    gj_adjustments = 0
    for key in comp_GJGoverner.keys():
        comp = model.getComponentByKey(key)
        comp_name = getattr(comp, 'label', key)
        
        # 若Ki参数过大，则将其统一修改为0.1
        if float(comp.args['Ki']) <= 0:
            old_value = comp.args['Ki']
            comp.args['Ki'] = str(0.1)
            logging.info(f"GJGoverner元件 {comp_name} 的 Ki 参数调整: {old_value} -> 0.1 (触发条件: Ki == 0)")
            gj_adjustments += 1
            
        # 若纯延时过大，则将其统一修改为0.95
        if float(comp.args['TW_DELAY']) > 0.95:
            old_value = comp.args['TW_DELAY']
            comp.args['TW_DELAY'] = str(0.95)
            logging.info(f"GJGoverner元件 {comp_name} 的 TW_DELAY 参数调整: {old_value} -> 0.95 (触发条件: TW_DELAY > 1)")
            gj_adjustments += 1
            
        if float(comp.args['TP_DELAY']) > 0.95:
            old_value = comp.args['TP_DELAY']
            comp.args['TP_DELAY'] = str(0.95)
            logging.info(f"GJGoverner元件 {comp_name} 的 TP_DELAY 参数调整: {old_value} -> 0.95 (触发条件: TP_DELAY > 1)")
            gj_adjustments += 1
            
        if float(comp.args['TW2_delay']) > 0.95:
            old_value = comp.args['TW2_delay']
            comp.args['TW2_delay'] = str(0.95)
            logging.info(f"GJGoverner元件 {comp_name} 的 TW2_delay 参数调整: {old_value} -> 0.95 (触发条件: TW2_delay > 1)")
            gj_adjustments += 1
            
        if float(comp.args['TW_DELAY_PID']) > 1:
            old_value = comp.args['TW_DELAY_PID']
            comp.args['TW_DELAY_PID'] = str(0.95)
            logging.info(f"GJGoverner元件 {comp_name} 的 TW2_delay 参数调整: {old_value} -> 0.95 (触发条件: TW2_delay > 1)")
            gj_adjustments += 1

        if float(comp.args['INTG_MAX']) <= 0:
            old_value = comp.args['INTG_MAX']
            comp.args['INTG_MAX'] = str(1)
            logging.info(f"GJGoverner元件 {comp_name} 的 INTG_MAX 参数调整: {old_value} -> 1 (触发条件: INTG_MAX <= 0)")
            gj_adjustments += 1

        if float(comp.args['INTG_MIN']) >= 0:
            old_value = comp.args['INTG_MIN']
            comp.args['INTG_MIN'] = str(-1)
            logging.info(f"GJGoverner元件 {comp_name} 的 INTG_MIN 参数调整: {old_value} -> -1 (触发条件: INTG_MIN >= 0)")
            gj_adjustments += 1

        if float(comp.args['PID_MAX']) <= 0:
            old_value = comp.args['PID_MAX']
            comp.args['PID_MAX'] = str(1)
            logging.info(f"GJGoverner元件 {comp_name} 的 PID_MAX 参数调整: {old_value} -> 1 (触发条件: PID_MAX <= 0)")
            gj_adjustments += 1

        if float(comp.args['PID_MIN']) >= 0:
            old_value = comp.args['PID_MIN']
            comp.args['PID_MIN'] = str(-1)
            logging.info(f"GJGoverner元件 {comp_name} 的 PID_MIN 参数调整: {old_value} -> -1 (触发条件: PID_MIN >= 0)")
            gj_adjustments += 1

        if float(comp.args['DPup']) <= 0:
            old_value = comp.args['DPup']
            comp.args['DPup'] = str(99999999)
            logging.info(f"GJGoverner元件 {comp_name} 的 DPup 参数调整: {old_value} -> 999999 (触发条件: DPup <= 0)")
            gj_adjustments += 1

        if float(comp.args['DPdown']) >= 0:
            old_value = comp.args['DPdown']
            comp.args['DPdown'] = str(-99999999)
            logging.info(f"GJGoverner元件 {comp_name} 的 DPdown 参数调整: {old_value} -> -999999 (触发条件: DPdown >= 0)")
            gj_adjustments += 1

        if float(comp.args['Wmax']) <= 0:
            old_value = comp.args['Wmax']
            comp.args['Wmax'] = str(0.02)
            logging.info(f"GJGoverner元件 {comp_name} 的 Wmax 参数调整: {old_value} -> 0.02 (触发条件: Wmax <= 0)")
            gj_adjustments += 1

        if float(comp.args['Wmin']) >= 0:
            old_value = comp.args['Wmin']
            comp.args['Wmin'] = str(-0.02)
            logging.info(f"GJGoverner元件 {comp_name} 的 Wmin 参数调整: {old_value} -> -0.02 (触发条件: Wmin >= 0)")
            gj_adjustments += 1

    
    logging.info(f"GJGoverner元件调整完成，共进行了 {gj_adjustments} 次调整")
            
    # 获取模型中所有GNGoverner元件的实例
    comp_GNGoverner = model.getComponentsByRid('model/CloudPSS/_GNGoverner')
    logging.info(f"开始检查GNGoverner元件，共 {len(comp_GNGoverner)} 个")
    
    gn_adjustments = 0
    for key in comp_GNGoverner.keys():
        comp = model.getComponentByKey(key)
        comp_name = getattr(comp, 'label', key)
        
        # 若Ki参数过大，则将其统一修改为0.1
        if float(comp.args['Ki']) == 0:
            old_value = comp.args['Ki']
            comp.args['Ki'] = str(0.1)
            logging.info(f"GNGoverner元件 {comp_name} 的 Ki 参数调整: {old_value} -> 0.1 (触发条件: Ki == 0)")
            gn_adjustments += 1

        if float(comp.args['INTG_MAX']) <= 0:
            old_value = comp.args['INTG_MAX']
            comp.args['INTG_MAX'] = str(1)
            logging.info(f"GNGoverner元件 {comp_name} 的 INTG_MAX 参数调整: {old_value} -> 1 (触发条件: INTG_MAX <= 0")
            gn_adjustments += 1

        if float(comp.args['INTG_MIN']) >= 0:
            old_value = comp.args['INTG_MIN']
            comp.args['INTG_MIN'] = str(-1)
            logging.info(f"GNGoverner元件 {comp_name} 的 INTG_MIN 参数调整: {old_value} -> -1 (触发条件: INTG_MIN >= 0)")
            gn_adjustments += 1

        if float(comp.args['PID_MAX']) <= 0:
            old_value = comp.args['PID_MAX']
            comp.args['PID_MAX'] = str(1)
            logging.info(f"GNGoverner元件 {comp_name} 的 PID_MAX 参数调整: {old_value} -> 1 (触发条件: PID_MAX <= 0)")
            gn_adjustments += 1

        if float(comp.args['PID_MIN']) >= 0:
            old_value = comp.args['PID_MIN']
            comp.args['PID_MIN'] = str(-1)
            logging.info(f"GNGoverner元件 {comp_name} 的 PID_MIN 参数调整: {old_value} -> -1 (触发条件: PID_MIN >= 0)")
            gn_adjustments += 1

        if float(comp.args['PID_MAX2']) <= 0:
            old_value = comp.args['PID_MAX2']
            comp.args['PID_MAX2'] = str(1)
            logging.info(f"GNGoverner元件 {comp_name} 的 PID_MAX2 参数调整: {old_value} -> 1 (触发条件: PID_MAX2 <= 0)")
            gn_adjustments += 1

        if float(comp.args['PID_MIN2']) >= 0:
            old_value = comp.args['PID_MIN2']
            comp.args['PID_MIN2'] = str(-1)
            logging.info(f"GNGoverner元件 {comp_name} 的 PID_MIN2 参数调整: {old_value} -> -1 (触发条件: PID_MIN2 >= 0)")
            gn_adjustments += 1

        if float(comp.args['INTG_MAX2']) <= 0:
            old_value = comp.args['INTG_MAX2']
            comp.args['INTG_MAX2'] = str(1)
            logging.info(f"GNGoverner元件 {comp_name} 的 INTG_MAX2 参数调整: {old_value} -> 1 (触发条件: INTG_MAX2 <= 0")
            gn_adjustments += 1

        if float(comp.args['INTG_MIN2']) >= 0:
            old_value = comp.args['INTG_MIN2']
            comp.args['INTG_MIN2'] = str(-1)
            logging.info(f"GNGoverner元件 {comp_name} 的 INTG_MIN2 参数调整: {old_value} -> -1 (触发条件: INTG_MIN2 >= 0)")
            gn_adjustments += 1

        if float(comp.args['DY_MAX']) <= 0:
            old_value = comp.args['DY_MAX']
            comp.args['DY_MAX'] = str(1)
            logging.info(f"GNGoverner元件 {comp_name} 的 DY_MAX 参数调整: {old_value} -> 1 (触发条件: DY_MAX <=0)")
            gn_adjustments += 1

        if float(comp.args['DY_MIN']) >= 0:
            old_value = comp.args['DY_MIN']
            comp.args['DY_MIN'] = str(-1)
            logging.info(f"GNGoverner元件 {comp_name} 的 DY_MIN 参数调整: {old_value} -> -1 (触发条件: DY_MIN >= 0)")
            gn_adjustments += 1
    
    logging.info(f"GNGoverner元件调整完成，共进行了 {gn_adjustments} 次调整")
            
    # 获取模型中所有PVStation元件的实例
    comp_PVStation = model.getComponentsByRid('model/CloudPSS/PVStation')
    logging.info(f"开始检查PVStation元件，共 {len(comp_PVStation)} 个")
    
    pv_adjustments = 0
    for key in comp_PVStation.keys():
        comp = model.getComponentByKey(key)
        comp_name = getattr(comp, 'label', key)
        
        # # 若有功、无功初值参数过小，则将其统一修改为0.1
        # if float(comp.args['PG0']) <= 0:
        #     old_value = comp.args['PG0']
        #     comp.args['PG0'] = str(0.1)
        #     logging.info(f"PVStation元件 {comp_name} 的 PG0 参数调整: {old_value} -> 0.1 (触发条件: PG0 <= 0)")
        #     pv_adjustments += 1
            
        # if float(comp.args['QG0']) <= 0:
        #     old_value = comp.args['QG0']
        #     comp.args['QG0'] = str(0.001)
        #     logging.info(f"PVStation元件 {comp_name} 的 QG0 参数调整: {old_value} -> 0.1 (触发条件: QG0 <= 0)")
        #     pv_adjustments += 1
    
    logging.info(f"PVStation元件调整完成，共进行了 {pv_adjustments} 次调整")
    
    # 获取模型中所有DFIG_WindFarm_Equivalent_Model元件的实例
    comp_DFIG = model.getComponentsByRid('model/CloudPSS/DFIG_WindFarm_Equivalent_Model')
    logging.info(f"开始检查DFIG_WindFarm_Equivalent_Model元件，共 {len(comp_DFIG)} 个")
    
    dfig_adjustments = 0
    for key in comp_DFIG.keys():
        comp = model.getComponentByKey(key)
        comp_name = getattr(comp, 'label', key)
        
        # # 若有功、无功初值参数过小，则将其统一修改为0.1
        # if float(comp.args['P_cmd']) <= 0:
        #     old_value = comp.args['P_cmd']
        #     comp.args['P_cmd'] = str(10)    # 均为有名值MW, MVAR
        #     logging.info(f"DFIG_WindFarm元件 {comp_name} 的 P_cmd 参数调整: {old_value} -> 10 (触发条件: P_cmd <= 0)")
        #     dfig_adjustments += 1
            
        # if float(comp.args['Q_cmd']) <= 0:
        #     old_value = comp.args['Q_cmd']
        #     comp.args['Q_cmd'] = str(1)
        #     logging.info(f"DFIG_WindFarm元件 {comp_name} 的 Q_cmd 参数调整: {old_value} -> 1 (触发条件: Q_cmd <= 0)")
        #     dfig_adjustments += 1

        # # 台数
        # if float(comp.args['Num']) < np.ceil(float(comp.args['P_cmd'])/float(comp.args['Mrating'])):
        #     comp.args['Num'] = str(np.ceil(float(comp.args['P_cmd'])/float(comp.args['Mrating'])))
    
    logging.info(f"DFIG_WindFarm_Equivalent_Model元件调整完成，共进行了 {dfig_adjustments} 次调整")
            
            
    # 获取模型中所有WGSource元件的实例
    comp_GSource = model.getComponentsByRid('model/CloudPSS/WGSource')
    logging.info(f"开始检查WGSource元件，共 {len(comp_GSource)} 个")
    
    wg_adjustments = 0
    for key in comp_GSource.keys():
        comp = model.getComponentByKey(key)
        comp_name = getattr(comp, 'label', key)
        
        # # 若有功、无功初值参数过小，则将其统一修改为0.1
        # if float(comp.args['Pref_WF']) <= 0:
        #     old_value = comp.args['Pref_WF']
        #     comp.args['Pref_WF'] = str(10)    # 均为有名值MW, MVAR
        #     logging.info(f"WGSource元件 {comp_name} 的 Pref_WF 参数调整: {old_value} -> 10 (触发条件: Pref_WF <= 0)")
        #     wg_adjustments += 1
            
        # if float(comp.args['Qref_WF']) <= 0:
        #     old_value = comp.args['Qref_WF']
        #     comp.args['Qref_WF'] = str(1)
        #     logging.info(f"WGSource元件 {comp_name} 的 Qref_WF 参数调整: {old_value} -> 1 (触发条件: Qref_WF <= 0)")
        #     wg_adjustments += 1

        # # 台数
        # if float(comp.args['Num']) < np.ceil(float(comp.args['P_cmd'])/float(comp.args['Mrating'])):
        #     comp.args['Num'] = str(np.ceil(float(comp.args['P_cmd'])/float(comp.args['Mrating'])))
    
    logging.info(f"WGSource元件调整完成，共进行了 {wg_adjustments} 次调整")
        
        
    # 获取模型中所有电阻元件的实例
    comp_Resistor = model.getComponentsByRid('model/CloudPSS/newResistorRouter')
    logging.info(f"开始检查电阻元件，共 {len(comp_Resistor)} 个")

    resistor_adjustments = 0
    for key in comp_Resistor.keys():
        comp = model.getComponentByKey(key)
        comp_name = getattr(comp, 'label', key)
        name1 = comp.args['Name']
        # 不自动处理电阻元件
                    
    logging.info(f"电阻元件调整完成，共进行了 {resistor_adjustments} 次调整")
    

    # 获取模型中所有电感元件的实例
    comp_Inductor = model.getComponentsByRid('model/CloudPSS/newInductorRouter')
    logging.info(f"开始检查电感元件，共 {len(comp_Inductor)} 个")

    inductor_adjustments = 0
    for key in comp_Inductor.keys():
        comp = model.getComponentByKey(key)
        comp_name = getattr(comp, 'label', key)
        name = comp.args['Name']
        # 不自动处理电感元件

    logging.info(f"电感元件调整完成，共进行了 {inductor_adjustments} 次调整")
    
    
    # 计算总调整次数
    total_adjustments = (Gen_adjustments + transformer_adjustments + Vsource_adjustments + gm_adjustments + load_adjustments + 
                        lcc_adjustments + mnopqrst_adjustments + uv_adjustments + 
                        ga_adjustments + gi_adjustments + 
                        gj_adjustments + gn_adjustments + pv_adjustments + 
                        dfig_adjustments + wg_adjustments + resistor_adjustments + inductor_adjustments)
    
    logging.info("=== 设备参数调整总结 ===")
    logging.info(f"变压器元件调整: {transformer_adjustments} 次")
    logging.info(f"负荷元件调整: {load_adjustments} 次")
    logging.info(f"理想电压源元件调整: {Vsource_adjustments} 次")
    logging.info(f"LCC元件调整: {lcc_adjustments} 次")
    logging.info(f"E_F_MNOPQRST_Exciter元件调整: {mnopqrst_adjustments} 次")
    logging.info(f"UV_Exciter元件调整: {uv_adjustments} 次")
    logging.info(f"GAGoverner元件调整: {ga_adjustments} 次")
    logging.info(f"GMGoverner元件调整: {gm_adjustments} 次") 
    logging.info(f"GIGoverner元件调整: {gi_adjustments} 次")
    logging.info(f"GJGoverner元件调整: {gj_adjustments} 次")
    logging.info(f"GNGoverner元件调整: {gn_adjustments} 次")
    logging.info(f"PVStation元件调整: {pv_adjustments} 次")
    logging.info(f"DFIG_WindFarm元件调整: {dfig_adjustments} 次")
    logging.info(f"WGSource元件调整: {wg_adjustments} 次")
    logging.info(f"电阻元件调整: {resistor_adjustments} 次")
    logging.info(f"电感元件调整: {inductor_adjustments} 次")
    logging.info(f"总调整次数: {total_adjustments} 次")
    
    # 保存模型
    logging.info("开始保存模型...") 
    model.save()                          # 【若启用这一行，会直接覆盖原始文件！请谨慎！】
    logging.info("模型保存完成")
    logging.info("=== 设备参数调整日志结束 ===")
    print(f"调整完成！日志文件已保存为: {log_filename}")
    print(f"本次共进行了 {total_adjustments} 次参数调整")





