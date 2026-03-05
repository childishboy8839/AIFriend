<script setup>
import {ref, watch} from "vue";

const props = defineProps(['username'])//props 不能直接修改
const myUsername = ref(props.username)//创建一个副本

watch(() => props.username, newVal => {//监听 props 变化,保持父子数据同步
  myUsername.value = newVal
})

defineExpose({//子组件暴露给父组件
  myUsername,
})
</script>

<template>
  <fieldset class="fieldset">
    <label class="label text-base">用户名</label>
    <input v-model="myUsername" type="text" class="input w-108">
  </fieldset>
</template>

<style scoped>

</style>