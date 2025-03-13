<template>
  <div class="main-container">
    <div class="title-container">
      <h1>管理员页面</h1>
    </div>
    <div class="content-container">
      <p v-if="loading">加载中...</p>
      <div v-else>
        <el-tabs v-model="activeTab">
          <el-tab-pane label="人员管理">
            <el-table :data="users" style="width: 100%">
              <el-table-column prop="id" label="ID" />
              <el-table-column prop="username" label="用户名" />
              <el-table-column prop="is_active" label="是否活跃" />
              <el-table-column prop="is_admin" label="管理权限" />
              <el-table-column label="操作">
                <template #default="{ row }">
                  <el-button v-if="row.is_active&&!row.is_admin" type="danger" @click="active_update(row)">拉黑</el-button>
                  <el-button v-else-if="!row.is_active" type="success" @click="active_update(row)">恢复</el-button>
                </template>
              </el-table-column>
              <el-table-column label="操作">
                <template #default="{ row }">
                  <el-button v-if="!row.is_admin" type="success" @click="admin_update(row)">授权</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
          <el-tab-pane label="小说管理">
            <!-- 小说管理的画面内容 -->
            <el-table :data="novels" style="width: 100%">
              <el-table-column prop="id" label="ID" />
              <el-table-column prop="title" label="标题" />
              <el-table-column prop="is_visible" label="是否上架" />
              <el-table-column label="操作">
                <template #default="{ row }">
                  <el-button v-if="row.is_visible" type="danger" @click="visible_update(row)">下架小说</el-button>
                  <el-button v-else type="success" @click="visible_update(row)">重新上架小说</el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-tab-pane>
        </el-tabs>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';
import { ElTabs, ElTabPane, ElTable, ElTableColumn } from 'element-plus';

export default {
  name: "Administrator",
  components: {
    ElTabs,
    ElTabPane,
    ElTable,
    ElTableColumn
  },
  data() {
    return {
      users: [],
      novels: [],
      loading: true,
      activeTab: '人员管理' // 默认显示人员管理选项卡
    };
  },
  computed: {
    ...mapState(['token']),
  },
  mounted() {
    this.fetchUsers();
    this.fetchNovels();
  },
  methods: {
    async fetchUsers() {
      try {
        const token = this.token;
        const response = await axios.get(`${this.$backend}/admin/users`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.users = response.data;
        this.loading = false;
      } catch (error) {
        console.error('获取用户列表失败', error);
      }
    },
    async fetchNovels() {
      try {
        const token = this.token;
        const response = await axios.get(`${this.$backend}/admin/novels/`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.novels = response.data;
      } catch (error) {
        console.error('获取小说列表失败', error);
      }
    },
    async visible_update(row) {
      try {
        const token = this.token;
        const response = await axios.patch(`${this.$backend}/novels/${row.id}/visible/`,{}, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        console.log(row.is_visible);
        //更新本地数据状态
        const updatedNovelIndex = this.novels.findIndex(item => item.id === row.id);
        if (updatedNovelIndex !== -1) {
          this.novels[updatedNovelIndex].is_visible = !this.novels[updatedNovelIndex].is_visible;
        }
        //如果后端返回成功消息，将其显示在页面上
        this.message = response || '完结状态更新成功';
      } catch (error) {
        // 如果后端返回错误信息，也将其显示在页面上
        this.message = error.response || '完结状态更新失败';
        console.error('完结状态更新失败', error);
      }
    },
    async active_update(row) {
      try {
        const token = this.token;
        const response = await axios.patch(`${this.$backend}/users/${row.id}/activate/`,{}, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        //更新本地数据状态
        const updatedNovelIndex = this.users.findIndex(item => item.id === row.id);
        if (updatedNovelIndex !== -1) {
          this.users[updatedNovelIndex].is_active = !this.users[updatedNovelIndex].is_active;
        }
        //如果后端返回成功消息，将其显示在页面上
        this.message = response || '完结状态更新成功';
      } catch (error) {
        // 如果后端返回错误信息，也将其显示在页面上
        this.message = error.response || '完结状态更新失败';
        console.error('完结状态更新失败', error);
      }
    },
    async admin_update(row) {
      try {
        const token = this.token;
        const response = await axios.patch(`${this.$backend}/users/${row.id}/admin/`,{}, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        //更新本地数据状态
        const updatedNovelIndex = this.users.findIndex(item => item.id === row.id);
        if (updatedNovelIndex !== -1) {
          this.users[updatedNovelIndex].is_admin = !this.users[updatedNovelIndex].is_admin;
        }
        //如果后端返回成功消息，将其显示在页面上
        this.message = response || '完结状态更新成功';
      } catch (error) {
        // 如果后端返回错误信息，也将其显示在页面上
        this.message = error.response || '完结状态更新失败';
        console.error('完结状态更新失败', error);
      }
    }
  }
};
</script>

<style scoped>
.main-container {
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.title-container {
  margin-top: 50px;
  margin-bottom: 30px;
}

.content-container {
  width: 60%;
}
</style>