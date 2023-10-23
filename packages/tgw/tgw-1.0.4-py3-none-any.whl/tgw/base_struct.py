class ReplayCfg(object):
    def __init__(self) -> None:
        self.begin_date = 0 # int
        self.end_date = 0 # int
        self.begin_time = 0 # int
        self.end_time = 0 #int
        self.task_id = 0 # int
        self.req_codes = [] # list of tuple [(market, code), ...] like [101, '000001']
        self.cq_flag = 0
        self.cyc_type = 1
        self.auto_complete = 1
        self.replay_speed = 0
        self.cq_date = 0
        self.cyc_def = 0
        self.qj_flag = 0
        self.md_data_type = 0

class ReqFactorCfg(object):
    def __init__(self) -> None:
        self.task_id = 0
        self.factor_type = ''
        self.factor_sub_type = ''
        self.factor_name = ''
        self.begin_date = 0
        self.end_date = 0
        self.begin_time = 0
        self.end_time = 0
        self.security_code = ''
        self.market = 0
        self.category = 0
        self.count = 0
        self.key1 = ''
        self.key2 = ''
        