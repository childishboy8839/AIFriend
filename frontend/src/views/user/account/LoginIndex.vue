<script setup>
import {ref} from "vue";
import {useUserStore} from "@/stores/user.js";
import {useRouter} from "vue-router";
import api from "@/js/http/api.js";

const username=ref('')//先创建几个空变量用来接收输入
const password=ref('')
const errorMessage=ref('')

const user=useUserStore()
const router=useRouter()
async function handleLogin(){
  errorMessage.value=''   //清空错误信息
  if(!username.value.trim()) {    //username.value → 输入框内容, .trim() → 去掉空格
    errorMessage.value = "用户名不能为空"
  }
  else if(!password.value.trim()){
    errorMessage.value="密码不能为空"
  }//前端校验
  else{
    try{
      const res=await api.post('/api/user/account/login/',{
        username:username.value,
        password:password.value,
      })  //向后端发送用户的输入
      const data=res.data  //获取返回数据
      if(data.result==='success'){
        user.setAccessToken(data.access) //保存Token
        user.setUserInfo(data)  //保存用户信息
        await router.push({   //跳转到首页
          name: 'homepage-index'
        })
      }else{
        errorMessage.value=data.result
      }
    }catch (err){
      console.log(err)
    }
  }
}

</script>

<template>
  <div class="flex justify-center mt-30">
    <form @submit.prevent="handleLogin" class="fieldset bg-base-200 border-base-300 rounded-box w-xs border p-4">
      <label class="label">用户名</label>
      <input v-model="username" type="text" class="input" placeholder="用户名" />

      <label class="label">密码</label>
      <input v-model="password" type="password" class="input" placeholder="密码" />
      <p v-if="errorMessage" class="text-sm text-red-500 mt-1">{{errorMessage}}</p>
      <button  class="btn btn-neutral mt-4">登录</button>
      <div class="flex justify-end">
        <RouterLink :to="{name:'user-account-register-index'}" class="btn btn-sm btn-ghost text-gray-500">
          注册
        </RouterLink>
      </div>
    </form>
  </div>
</template>

<style scoped>

</style>