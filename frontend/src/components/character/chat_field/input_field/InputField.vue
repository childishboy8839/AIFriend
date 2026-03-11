<script setup>
import SendIcon from "@/components/character/icons/SendIcon.vue";
import MicIcon from "@/components/character/icons/MicIcon.vue";
import {onUnmounted, ref, useTemplateRef} from "vue";
import streamApi from "@/js/http/streamApi.js";
import Microphone from "@/components/character/chat_field/input_field/Microphone.vue";

//组件负责：1.用户输入消息 2.发送给后端聊天接口 3.接收流式AI回复 4.实时把AI回复追加到聊天框

const props = defineProps(['friendId'])//定义响应式变量
const emit = defineEmits(['pushBackMessage', 'addToLastMessage'])//定义事件，通知父组件有两个事件。pushBackMessage:新增一条消息。
                                                                            //addToLastMessage:流式更新AI回复
const inputRef = useTemplateRef('input-ref')//绑定，用于focus聚焦输入框
const message = ref('')//绑定输入框，用于接收内容
let processId=0 //用于记录版本号，方便用户随时打断输出

const showMic=ref(false)//用于决定是否显示麦克风


let mediaSource = null;
let sourceBuffer = null;
let audioPlayer = new Audio(); // 全局播放器实例
let audioQueue = [];           // 待写入 Buffer 的二进制队列
let isUpdating = false;        // Buffer 是否正在写入

const initAudioStream = () => {
    audioPlayer.pause();
    audioQueue = [];
    isUpdating = false;

    mediaSource = new MediaSource();
    audioPlayer.src = URL.createObjectURL(mediaSource);

    mediaSource.addEventListener('sourceopen', () => {
        try {
            sourceBuffer = mediaSource.addSourceBuffer('audio/mpeg');
            sourceBuffer.addEventListener('updateend', () => {
                isUpdating = false;
                processQueue();
            });
        } catch (e) {
            console.error("MSE AddSourceBuffer Error:", e);
        }
    });

    audioPlayer.play().catch(e => console.error("等待用户交互以播放音频"));
};

const processQueue = () => {
    if (isUpdating || audioQueue.length === 0 || !sourceBuffer || sourceBuffer.updating) {
        return;
    }

    isUpdating = true;
    const chunk = audioQueue.shift();
    try {
        sourceBuffer.appendBuffer(chunk);
    } catch (e) {
        console.error("SourceBuffer Append Error:", e);
        isUpdating = false;
    }
};

const stopAudio = () => {
    audioPlayer.pause();
    audioQueue = [];
    isUpdating = false;

    if (mediaSource) {
        if (mediaSource.readyState === 'open') {
            try {
                mediaSource.endOfStream();
            } catch (e) {
            }
        }
        mediaSource = null;
    }

    if (audioPlayer.src) {
        URL.revokeObjectURL(audioPlayer.src);
        audioPlayer.src = '';
    }
};

const handleAudioChunk = (base64Data) => {  // 将语音片段添加到播放器队列中
    try {
        const binaryString = atob(base64Data);
        const len = binaryString.length;
        const bytes = new Uint8Array(len);
        for (let i = 0; i < len; i++) {
            bytes[i] = binaryString.charCodeAt(i);
        }

        audioQueue.push(bytes);
        processQueue();
    } catch (e) {
        console.error("Base64 Decode Error:", e);
    }
};

onUnmounted(() => {
    audioPlayer.pause();
    audioPlayer.src = '';
});


function focus() {
  inputRef.value.focus()
}

async function handleSend(event,audio_msg) {//聊天入口函数
  let content
  if(audio_msg){
    content=audio_msg.trim()//获取语音消息
  }else{
    content = message.value.trim() //获取输入框的值
  }
  if (!content) return //空消息不能发送

  initAudioStream()

  const curId=++processId //记录现在的版本号
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
        if(curId!==processId) return //实现用户随时打断
        if (data.content) {//AI正在回复，会在消息后加上data.content，逐字回复
          emit('addToLastMessage', data.content)
        }
        if (data.audio){
          handleAudioChunk(data.audio)
        }
      },
      onerror(err) {//避免卡死
      },
    })
  } catch (err) {
  }
}
function close() {
  ++processId
  showMic.value=false
  stopAudio()
}
function handleStop(){ //打断音频
  ++processId
  stopAudio()
}
//暴露方法
defineExpose({
  focus,
  close,
})
</script>

<template>
  <form v-if="!showMic" @submit.prevent="handleSend" class="absolute bottom-4 left-2 h-12 w-86 flex items-center">
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
    <div @click="showMic=true" class="absolute right-10 w-8 h-8 flex justify-center items-center cursor-pointer">
      <MicIcon />
    </div>
  </form>
  <Microphone
      v-else
      @close="showMic=false"
      @send="handleSend"
      @stop="handleStop"
  />
</template>

<style scoped>

</style>
