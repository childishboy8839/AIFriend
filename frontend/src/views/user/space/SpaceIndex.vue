<script setup>
import {useRoute,useRouter} from "vue-router";

const route=useRoute()
</script>

<template>
个人主页:{{route.params.user_id}}
</template>

<style scoped>

</style>