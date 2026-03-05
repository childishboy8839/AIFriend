import {defineStore} from "pinia";
import {ref} from "vue";
//全局保存用户信息，所有页面都从这里读取用户信息
export const useUserStore=defineStore('user',()=> {
    const id=ref(0)
    const username=ref('')
    const photo=ref('')
    const profile=ref('')
    const accessToken=ref('')
    const hasPulledUserInfo=ref(false)
    function isLogin(){
        return !!accessToken.value  //必须带value
    }
    function setAccessToken(token){
        accessToken.value=token
    }
    function setUserInfo(data){
        id.value=data.user_id
        username.value=data.username
        photo.value=data.photo
        profile.value=data.profile
    }
    function logout(){
        id.value=0
        username.value=''
        photo.value=''
        profile.value=''
        accessToken.value=''
    }
     function setHasPulledUserInfo(newStatus) {
        hasPulledUserInfo.value = newStatus
    }

    return {
        id,
        username,
        photo,
        profile,
        isLogin,
        accessToken,
        setAccessToken,
        setUserInfo,
        logout,
        hasPulledUserInfo,
        setHasPulledUserInfo,
    }
})