import { createStore } from 'vuex';
import createPersistedState from 'vuex-persistedstate';

const store = createStore({
  state: {
    token: '',
    isLoggedIn: false,  // 添加一个表示用户登录状态的状态
    is_admin: false,    //是否是管理员
  },
  mutations: {
    setToken(state, newToken) {
      state.token = newToken;
      state.isLoggedIn = true;
    },
    setIsadmin(state,new_state_is_admin){
      state.is_admin = new_state_is_admin;
    },
    removeToken(state) {
      state.token = '';
      // 设置用户登录状态为 false
      state.isLoggedIn = false;
      state.is_admin = false;
    },
  },
  getters: {
    // 添加一个 getter 方法用于判断用户是否登录
    checkLoggedIn: state =>!!state.token,
  },
  plugins: [
    createPersistedState({
      storage: window.sessionStorage,
    }),
  ],
});

export default store;