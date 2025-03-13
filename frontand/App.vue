<template>
  <div class="totaltype" id="app">
    <el-menu class="left-menu" :default-active="activeIndex" mode="horizontal" @select="handleSelect"
      style="background-color: #F5F5F5;">
      <el-menu-item class="left-menu"index="1">主页</el-menu-item>>
      <el-menu-item v-if="isLoggedIn" index="6">个人信息</el-menu-item>
      <el-menu-item v-if="is_admin" index="7">管理员页面</el-menu-item>
      <el-menu-item v-if="isLoggedIn" index="5">登出</el-menu-item>
      <el-menu-item v-if="!isLoggedIn" index="2">登录</el-menu-item>
      <el-menu-item v-if="!isLoggedIn" index="3">注册</el-menu-item>
    </el-menu>
    <router-view />
  </div>
</template>

<script>
import { mapState } from 'vuex';

export default {
  data() {
    return {
      activeIndex: '1',
    };
  },
  computed: {
    ...mapState(['isLoggedIn', 'is_admin']),
  },
  methods: {
    handleSelect(key, keyPath) {
      if (key === '1') this.$router.push('/');
      if (key === '2') {
        this.$router.push('/login');
        this.activeIndex = '1';
      }
      if (key === '3') this.$router.push('/register');
      if (key === '5') {
        this.$store.commit('removeToken');
        this.$router.push('/');
      }
      if (key === '6') {
        this.$router.push('/users/me');
        this.activeIndex = '1';}
      if (key === '7') this.$router.push('/Administrator');

    },
  },
};
</script>

<style>
.left-menu {
  height: 40px; /* 根据你的需求调整宽度值 */
}
</style>