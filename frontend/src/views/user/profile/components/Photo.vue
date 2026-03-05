<script setup>
import {nextTick, onBeforeUnmount, ref, useTemplateRef, watch} from "vue";
import CameraIcon from "@/views/user/profile/components/icon/CameraIcon.vue";
import Croppie from 'croppie'
import 'croppie/croppie.css'

const props = defineProps(['photo'])//接收传入的属性
const myPhoto = ref(props.photo)

watch(() => props.photo, newVal => {
  myPhoto.value = newVal
})

const fileInputRef = useTemplateRef('file-input-ref') //隐藏的文件选择框
const modalRef = useTemplateRef('modal-ref')  //dialog 弹窗
const croppieRef = useTemplateRef('croppie-ref')  //裁剪容器
let croppie = null

async function openModal(photo) {
  modalRef.value.showModal()  //打开弹窗
  await nextTick()

  if (!croppie) { //只初始化一次
    croppie = new Croppie(croppieRef.value, {
      viewport: {width: 200, height: 200, type: 'square'},
      boundary: {width: 300, height: 300},
      enableOrientation: true,
      enforceBoundary: true,
    })
  }

  croppie.bind({
    url: photo,
  })
}

async function crop() {
  if (!croppie) return

  myPhoto.value = await croppie.result({
    type: 'base64',
    size: 'viewport',
  })//等待裁剪结果

  modalRef.value.close()//关闭弹窗
}

function onFileChange(e) {
  const file = e.target.files[0]
  e.target.value = ''
  if (!file) return

  const reader = new FileReader()//获取文件
  reader.onload = () => {
    openModal(reader.result)
  }

  reader.readAsDataURL(file)
}

onBeforeUnmount(() => {
  croppie?.destroy()  //销毁组件
})

defineExpose({
  myPhoto,
})
</script>

<template>
  <div class="flex justify-center">
    <div class="avatar relative">
      <div class="w-28 rounded-full">
        <img :src="myPhoto" alt="">
      </div>
      <div @click="fileInputRef.click()" class="absolute left-0 top-0 w-28 h-28 flex justify-center items-center bg-black/20 rounded-full cursor-pointer">
        <CameraIcon />
      </div>
    </div>
  </div>

  <input ref="file-input-ref" type="file" accept="image/*" class="hidden" @change="onFileChange">

  <dialog ref="modal-ref" class="modal">
    <div class="modal-box transition-none">
      <button @click="modalRef.close()" class="btn btn-circle btn-sm btn-ghost absolute right-2 top-2">✕</button>

      <div ref="croppie-ref" class="flex flex-col justify-center my-4"></div>

      <div class="modal-action">
        <button @click="modalRef.close()" class="btn">取消</button>
        <button @click="crop" class="btn btn-neutral">确定</button>
      </div>
    </div>
  </dialog>
</template>

<style scoped>

</style>