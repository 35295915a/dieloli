import copy
from Script.Core import cache_contorl, constant
from Script.Design import (
    game_time,
    character_behavior,
    map_handle,
    character_move,
    character
)


@character_behavior.add_behavior(
    "Teacher", constant.CharacterStatus.STATUS_ARDER
)
def arder_behavior(character_id: int):
    """
    教师休闲状态行为
    Keyword arguments:
    character_id -- 角色id
    """
    character_data = cache_contorl.character_data[character_id]
    now_time_slice = game_time.get_now_time_slice(character_id)
    if now_time_slice["InCourse"]:
        character.init_character_behavior_start_time(character_id)
        if character_data.position != map_handle.get_map_system_path_for_str(
            character_data.classroom
        ):
            _, _, move_path, move_time = character_move.character_move(
                character_id,
                map_handle.get_map_system_path_for_str(
                    character_data.classroom
                ),
            )
            character_data.behavior["BehaviorId"] = constant.Behavior.MOVE
            character_data.behavior["MoveTarget"] = move_path
            character_data.behavior["Duration"] = move_time
            character_data.state = constant.CharacterStatus.STATUS_MOVE
        else:
            character_data.behavior[
                "BehaviorId"
            ] = constant.Behavior.ATTEND_CLASS
            character_data.behavior["Duration"] = now_time_slice["EndCourse"]
            character_data.behavior["MoveTarget"] = []
            character_data.state = constant.CharacterStatus.STATUS_ATTEND_CLASS
    elif now_time_slice["TimeSlice"] == constant.TimeSlice.TIME_BREAKFAST:
        if character_data.status["BodyFeeling"]["Hunger"] > 16:
            now_scene_str = map_handle.get_map_system_path_str_for_list(character_data.position)
            now_scene_data = cache_contorl.scene_data[now_scene_str]
            if now_scene_data["SceneTag"] == "Cafeteria":
                pass
            elif now_scene_data["SceneTag"] == "Restaurant":
                pass
            else:
                pass
    return 1