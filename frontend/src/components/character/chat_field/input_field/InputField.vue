<script setup>
import SendIcon from "@/components/character/icons/SendIcon.vue";
import MicIcon from "@/components/character/icons/MicIcon.vue";
import {ref, useTemplateRef} from "vue";
import streamApi from "@/js/http/streamApi.js";

//组件负责：1.用户输入消息 2.发送给后端聊天接口 3.接收流式AI回复 4.实时把AI回复追加到聊天框

const props = defineProps(['friendId'])//定义响应式变量
const emit = defineEmits(['pushBackMessage', 'addToLastMessage'])//定义事件，通知父组件有两个事件。pushBackMessage:新增一条消息。
                                                                            //addToLastMessage:流式更新AI回复
const inputRef = useTemplateRef('input-ref')//绑定，用于focus聚焦输入框
const message = ref('')//绑定输入框，用于接收内容
let isProcessing = false //防止重复输入

function focus() {
  inputRef.value.focus()
}

async function handleSend() {//聊天入口函数
  if (isProcessing) return //判断是否还在发送中
  isProcessing = true

  const content = message.value.trim() //获取输入框的值
  if (!content) return //空消息不能发送
  message.value = '' //将输入框清空

  emit('pushBackMessage', {role: 'user', content: content, id: crypto.randomUUID()})//先显示用户消息
  emit('pushBackMessage', {role: 'ai', content: '', id: crypto.randomUUID()})//预创建AI消息

  try {
    await streamApi('/api/friend/message/chat/', {//发生聊天请求
      body: {//数据,发送friend_id,message
        friend_id: props.friendId,
        message: content,
      },
      onmessage(data, isDone) {//接受流式消息
        if (isDone) {//AI回复完消息，可以继续发送
          isProcessing = false
        } else if (data.content) {//AI正在回复，会在消息后加上data.content，逐字回复
          emit('addToLastMessage', data.content)
        }
      },
      onerror(err) {//避免卡死
        isProcessing = false
      },
    })
  } catch (err) {
    isProcessing = false
  }
}
//暴露方法
defineExpose({
  focus,
})
</script>

<template>
  <form @submit.prevent="handleSend" class="absolute bottom-4 left-2 h-12 w-86 flex items-center">
    <input
        ref="input-ref"
        v-model="message"
        class="input bg-black/30 backdrop-blur-sm text-white text-base w-full h-full rounded-2xl pr-20"
        type="text"
        placeholder="文本输入..."
    >
    <div @click="handleSend" class="absolute right-2 w-8 h-8 flex justify-center items-center cursor-pointer">
      <SendIcon />
    </div>
    <div class="absolute right-10 w-8 h-8 flex justify-center items-center cursor-pointer">
      <MicIcon />
    </div>
  </form>
</template>

<style scoped>

</style>
