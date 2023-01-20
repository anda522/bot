from nonebot import get_driver
from pydantic import BaseModel, Extra
from pathlib import Path


class Config(BaseModel, extra=Extra.ignore):

    callback_notice: bool = True
    ban_rand_time_min: int = 60  # 随机禁言最短时间(s) default: 1分钟
    ban_rand_time_max: int = 24 * 60 * 60  # 随机禁言最长时间(s) default: 1天

    config_path = Path() / 'data' / 'group' / 'config'
    config_admin = config_path / 'admin.json'
    config_group_admin = config_path / 'group_admin.json'
    word_path = config_path / 'word_config.txt'
    words_contents_path = config_path / 'words'
    limit_word_path = config_path / '违禁词.txt'
    switcher_path = config_path / '开关.json'
    template_path = config_path / 'template'
    stop_words_path = config_path / 'stop_words'
    wordcloud_bg_path = config_path / 'wordcloud_bg'
    user_violation_info_path = config_path / '群内用户违规信息'
    group_message_data_path = config_path / '群消息数据'
    error_path = config_path / 'admin插件错误数据'
    broadcast_avoid_path = config_path / '广播排除群聊.json'
    black_list_path = config_path / 'black_list.json'

    res_path = Path() / 'data' / 'group' / 'resource'
    re_img_path = res_path / 'imgs'
    ttf_path = res_path / 'msyhblod.ttf'

    welcome_path = Path() / 'data' / 'group' / 'welcome.txt'
    admin_funcs = {
        'admin': ['管理', '踢', '禁', '改', '基础群管'],
        'requests': ['审批', '加群审批', '加群', '自动审批'],
        'wordcloud': ['群词云', '词云', 'wordcloud'],
        'word_analyze': ['消息记录', '群消息记录', '发言记录'],
        'broadcast': ['广播消息', '群广播', '广播'],
        'auto_ban': ['违禁词', '违禁词检测'],
        'group_msg': ['早安晚安', '早安', '晚安'],
        'particular_e_notice': ['事件通知', '变动通知', '事件提醒'],
        'group_recall': ['防撤回', '防止撤回']
    }

    # TODO 后续在这里对功能加 {‘default': True} 以便于初始化时自动设置开关状态
    funcs_name_cn = ['基础群管', '加群审批', '群词云', '违禁词检测']

    time_scop_map = {
        0: [0, 5 * 60],
        1: [5 * 60, 10 * 60],
        2: [10 * 60, 30 * 60],
        3: [30 * 60, 10 * 60 * 60],
        4: [10 * 60 * 60, 24 * 60 * 60],
        5: [24 * 60 * 60, 7 * 24 * 60 * 60],
        6: [7 * 24 * 60 * 60, 14 * 24 * 60 * 60],
        7: [14 * 24 * 60 * 60, 2591999]
    }


driver = get_driver()
global_config = driver.config
plugin_config = Config.parse_obj(global_config)
