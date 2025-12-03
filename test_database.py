from supabase import create_client, Client

SUPABASE_URL = "https://vwrpxjnpjuwquwhjkhwl.supabase.co"
SUPABASE_KEY = "sb_publishable_UpJgHYq4RCgFqkAhlMolyg_RhnziVgS"

# 创建Supabase客户端
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# 获取直播状态
def getLiveState(name):
    response = supabase.table("live_state").select("is_on_live").eq("name",name).execute().data
    return response[0]["is_on_live"]

# 获取录播状态
def getRecordState(name):
    response = supabase.table("live_state").select("is_on_record").eq("name",name).execute().data
    return response[0]["is_on_record"]

# 获取录播权限
def getRecordPermission(name):
    response = supabase.table("live_state").select("enable_record").eq("name",name).execute().data
    return response[0]["enable_record"]

# 获取主播名单
def getAllStreamer():
    response = supabase.table("live_state").select("name").execute().data
    streamer_list = [item["name"] for item in response if item.get("name")]
    return streamer_list

# 修改直播状态
def updateLiveState(name,state):
    response = supabase.table("live_state").update({"is_on_live": state}).eq("name",name).execute().data
    return True if response else False

# 修改录播状态
def updateRecordState(name,state):
    response = supabase.table("live_state").update({"is_on_record": state}).eq("name",name).execute().data
    return True if response else False
