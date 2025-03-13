<template>
  <div class="login-container">
    <h2 class="login-h2">欢迎您的登录</h2>
    <p class="login-p">您将登录的是:笔趣阁</p>
    <input type="text" v-model="form.account" placeholder="账号" class="login-input" />
    <input type="password" v-model="form.password" placeholder="密码" class="login-input" />
    <button @click="submitForm" class="login-button">登录</button>
    <div class="register-link">
      <span class="login-register-span">还没有账号？</span>
      <el-link class="login-register-el" href="/register">去注册</el-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { ElMessageBox } from 'element-plus';

export default {
  name: "Login",
  data() {
    return {
      form: {
        account: "",
        password: "",
      },
      message: "",
    };
  },
  methods: {
    async submitForm() {
      const formData = new FormData();
      formData.append('username', this.form.account);
      formData.append('password', this.form.password);
      try {
        let res = await axios.post(`${this.$backend}/token`, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        });
        if (res.data.access_token !== '') {
          console.log('登录成功');
          this.$store.commit('setToken', res.data.access_token);
          this.$store.commit('setIsadmin', res.data.is_admin);
          if (res.data.is_admin) {
            ElMessageBox.confirm('欢迎登录，尊敬的管理员，是否现在进入管理员页面？', '确认', {
              confirmButtonText: '是',
              cancelButtonText: '否',
            })
              .then(() => {
                this.$router.push('/Administrator');
              })
              .catch(() => {
                this.$router.push('/');
              });
          } else {
            this.$router.push('/');
          }
        } else {
          this.message = "Password error";
        }
      } catch (error) {
        this.message = "An error occurred during login.";
      }
    },
  },
};
</script>

<style>
html,
body {
  height: 100%;
  margin: 0;
}

.login-container {
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

.login-h2 {
  margin-bottom: 10px;
  font-size: 24px;
}

.login-p {
  margin-bottom: 20px;
  font-size: 20px;
}

.login-input {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 3px;
  font-size: 20px;
}

.login-button {
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

.login-register-span {
  margin-right: 10px;
  font-size: 15px;
}

.login-register-el {
  color: #007bff;
  text-decoration: none;
  font-size: 30px;
}
</style>