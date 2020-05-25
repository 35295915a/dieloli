from functools import wraps
from Script.Core import text_loading, era_print, constant, cache_contorl
from Script.Design import game_time, update


handle_instruct_data = {}
""" 指令处理数据 """


def handle_instruct(instruct: str):
    """
    处理执行指令
    Keyword arguments:
    instruct -- 指令id
    """
    if instruct in handle_instruct_data:
        handle_instruct_data[instruct](instruct)


def add_instruct(instruct: str):
    """
    添加指令处理
    Keyword arguments:
    instruct -- 指令id
    """

    def decorator(func):
        @wraps(func)
        def return_wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        handle_instruct_data[instruct] = return_wrapper
        return return_wrapper

    return decorator


def handle_unknown_instruct():
    """
    处理未定义指令
    """
    era_print.line_feed_print(
        text_loading.get_text_data(constant.FilePath.MESSAGE_PATH, "42")
    )


@add_instruct("Rest")
def handle_rest():
    """
    处理休息指令
    """
    cache_contorl.character_data[0].behavior[
        "StartTime"
    ] = cache_contorl.game_time
    cache_contorl.character_data[0].behavior["Duration"] = 10
    cache_contorl.character_data[0].behavior[
        "BehaviorId"
    ] = constant.Behavior.REST
    cache_contorl.character_data[
        0
    ].state = constant.CharacterStatus.STATUS_REST
    if (
        cache_contorl.character_data[0].hit_point
        > cache_contorl.character_data[0].hit_point_max
    ):
        cache_contorl.character_data[
            0
        ].hit_point = cache_contorl.character_data[0].hit_point_max
    target_character = cache_contorl.character_data[
        cache_contorl.now_character_id
    ]
    if (
        target_character.state == constant.CharacterStatus.STATUS_ARDER
        and target_character.behavior["BehaviorId"]
        == constant.Behavior.SHARE_BLANKLY
    ):
        target_character.state = constant.CharacterStatus.STATUS_REST
        target_character.behavior["StartTime"] = cache_contorl.game_time
        target_character.behavior["Duration"] = 10
        target_character.behavior["BehaviorId"] = constant.Behavior.REST
    game_time.sub_time_now(10)
    update.game_update_flow()
