<script setup>
import Message from "@/components/character/chat_field/chat_history/message/Message.vue";
import {nextTick, onBeforeUnmount, onMounted, useTemplateRef} from "vue";
import api from "@/js/http/api.js";
//1 显示聊天记录,2 向上滚动时加载更早的聊天记录,3 保持滚动位置不跳动,4 渲染每一条 Message.vue
const props = defineProps(['history', 'friendId', 'character']) //父组件传入数据
const emit = defineEmits(['pushFrontMessage'])//通知父组件往聊天记录前面添加消息
const scrollRef = useTemplateRef('scroll-ref')//聊天滚动区域
const sentinelRef = useTemplateRef('sentinel-ref')//顶部哨兵
let isLoading = false
let hasMessages = true//顶部哨兵
let lastMessageId = 0//最后加载到的消息ID

function checkSentinelVisible() {  // 判断哨兵是否能被看到
  if (!sentinelRef.value) return false

  const sentinelRect = sentinelRef.value.getBoundingClientRect()//哨兵位置
  const scrollRect = scrollRef.value.getBoundingClientRect()//滚动区域位置
  return sentinelRect.top < scrollRect.bottom && sentinelRect.bottom > scrollRect.top//判断是否出现在滚动区域
}

async function loadMore() { //聊天历史加载
  if (isLoading || !hasMessages) return
  isLoading = true

  let newMessages = []
  try {
    const res = await api.get('/api/friend/message/get_history/', {//请求历史记录
      params: {
        last_message_id: lastMessageId,
        friend_id: props.friendId,
      }
    })
    const data = res.data
    if (data.result === 'success') {
      newMessages = data.messages//获取新的历史消息
    }
  } catch (err) {
  } finally {
    isLoading = false

    if (newMessages.length === 0) {
      hasMessages = false
    } else {
      const oldHeight = scrollRef.value.scrollHeight
      const oldTop = scrollRef.value.scrollTop

      for (const m of newMessages) {//获取每一条消息
        emit('pushFrontMessage', {
          role: 'ai',
          content: m.output,
          id: crypto.randomUUID(),
        })
        emit('pushFrontMessage', {
          role: 'user',
          content: m.user_message,
          id: crypto.randomUUID(),
        })
        lastMessageId = m.id
      }

      await nextTick()//等待message更新

      const newHeight = scrollRef.value.scrollHeight//更新后的位置
      scrollRef.value.scrollTop = oldTop + newHeight - oldHeight//修正滚动位置

      if (checkSentinelVisible()) {
        await loadMore()
      }
    }
  }
}

let observer = null
onMounted(async () => {
  await loadMore()

  observer = new IntersectionObserver(//自动加载
    entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          loadMore()
        }
      })
    },
    {root: null, rootMargin: '2px', threshold: 0}
  )

  observer.observe(sentinelRef.value)
})

onBeforeUnmount(() => {
  observer?.disconnect()
})

async function scrollToBottom() {//滚动到聊天底部
  await nextTick()

  scrollRef.value.scrollTop = scrollRef.value.scrollHeight
}

defineExpose({
  scrollToBottom
})
</script>

<template>
  <div ref="scroll-ref" class="absolute top-18 left-0 w-90 h-112 overflow-y-scroll no-scrollbar">
    <div ref="sentinel-ref" class="h-2"></div>
    <Message
        v-for="message in history"
        :key="message.id"
        :message="message"
        :character="character"
    />
  </div>
</template>

<style scoped>
/* 隐藏 Chrome, Safari 和 Opera 的滚动条 */
.no-scrollbar::-webkit-scrollbar {
  display: none;
}

/* 隐藏 IE, Edge 和 Firefox 的滚动条 */
.no-scrollbar {
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
}
</style>
