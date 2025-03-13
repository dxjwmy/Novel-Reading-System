<template>
  <div class="register-container">
    <h2 class="register-h2">欢迎注册</h2>
    <p class="register-p">您正在注册笔趣阁账号</p>
    <input type="text" v-model="username" placeholder="用户名" class="register-input"/>
    <input type="text" v-model="account" placeholder="账号" class="register-input"/>
    <input type="password" v-model="password" placeholder="密码" class="register-input"/>
    <input type="password" v-model="confirmPassword" placeholder="确认密码" class="register-input"/>
    <button @click="submitForm" class="register-button">注册</button>
    <div class="login-link">
      <span class="register-login-span">已有账号？</span>
      <el-link class="register-login-el" href="/login">去登录</el-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessage, ElMessageBox } from 'element-plus';
import router from '@/router';

export default {
  name: "Register",
  data() {
    return {
      form: {
        account: "",
        password: "",
        username: "",
      },
      confirmPassword:"",
      message: "",
    };
  },
  methods: {
    async submitForm() {
      // const { username, account, password } = this.form;
      // if (!username ||!account ||!password) {
      //   // 使用弹窗提醒
      //   ElMessageBox.alert('用户名、账号和密码都不能为空', '提示', {
      //     confirmButtonText: '确定',
      //   });
      //   return;
      // }
      console.log('注册反馈1:', this.password);
      console.log('注册反馈2:', this.confirmPassword);
      if (this.password!= this.confirmPassword) {
        // 密码不一致时的处理，可以弹出提示框
        alert('两次输入的密码不一致，请重新输入。');
        return;
      }
      try {
        let res = await axios.post(`${this.$backend}/register`, {
          "username": this.username,
          "password": this.password,
          "account": this.account
        }, {
          'Content-type': 'application/json'
        });
        this.message = res.data.message;
        ElMessage.success('注册成功！');
        router.push('/login');
      } catch (error) {
        this.message = error.response.data.detail || '注册失败，请稍后重试。';
      }
    },
  },
};
</script>

<style>
html, body {
  height: 100%;
  margin: 0;
}

.register-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  max-width: 400px;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.register-h2 {
  margin-bottom: 10px;
  font-size: 24px;
}

.register-p {
  margin-bottom: 20px;
  font-size: 20px;
}

.register-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 3px;
  font-size: 20px;
}

.register-button {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  font-size: 20px;
}

.register-link {
  display: flex;
  align-items: center;
  margin-top: 10px;
  font-size: 20px;
  justify-content: flex-end;
  margin-right: 10px;
}

.register-login-span {
  margin-right: 10px;
  font-size: 15px;
}

.register-login-el {
  color: #007bff;
  text-decoration: none;
  font-size: 30px;
}
</style>