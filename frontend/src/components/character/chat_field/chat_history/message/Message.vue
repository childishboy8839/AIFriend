<script setup>


//负责渲染一条聊天消息
import {useUserStore} from "@/stores/user.js";

defineProps(['message', 'character'])//接收父组件发来的消息 message是聊天的信息，character是角色信息，用来显示头像等

const user = useUserStore()
</script>

<template>
  <div v-if="message.content">
    <div v-if="message.role === 'ai'" class="chat chat-start">
      <div class="chat-image avatar">
        <div class="w-10 rounded-full">
          <img :src="character.photo" alt="">
        </div>
      </div>
      <div class="chat-bubble whitespace-pre-wrap break-all">{{ message.content }}</div>
    </div>
    <div v-else class="chat chat-end">
      <div class="chat-image avatar">
        <div class="w-10 rounded-full">
          <img :src="user.photo" alt="">>
        </div>
      </div>
      <div class="chat-bubble chat-bubble-success whitespace-pre-wrap break-all">{{ message.content }}</div>
    </div>
  </div>
</template>

<style scoped>

</style>
