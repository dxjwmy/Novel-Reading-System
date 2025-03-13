<template>
  <div>
    <div style="margin-top: 10px;"> </div>
    <h2 style=" text-indent: 2em;">个人信息</h2>
    <el-row v-if="loading">
      <el-col>
        <p>加载中...</p>
      </el-col>
    </el-row>
    <el-row v-else>
      <el-col>
        <p style="font-size: 20px; text-indent: 2em;">用户名：{{ user.username }}</p>
        <p style="font-size: 20px; text-indent: 2em;">账号：{{ user.account }}</p>
        <div style="margin-top: 100px;"> </div>
        <div v-if="Array.isArray(user.novels) && user.novels.length > 0">
          <h2>我的作品：</h2>
          <el-table :data="user.novels" style="width: 100%">
            <el-table-column label="标题" prop="title">
              <template #default="{ row }">
                <a :style="{ fontSize: '18px', color: row.isHovered ? 'blue' : '' }" @mouseenter="onHover(row, true)"
                  @mouseleave="onHover(row, false)" @click="goToNovelPage(row.id)">{{ row.title }}</a>
              </template>
            </el-table-column>
            <!--<el-table-column label="作者" prop="author_name"></el-table-column>-->
            <el-table-column label="分类" prop="category"></el-table-column>
            <el-table-column label="完结状态">
              <template #default="{ row }">
                <span @click="confirmUpdate(row)" :style="{ cursor: 'pointer' }">{{ row.is_finished ? '已完结' : '未完结'
                  }}</span>
              </template>
            </el-table-column>
            <el-table-column label="当前章节" prop="current_chapter"></el-table-column>
            <el-table-column label="当前字数" prop="word_count"></el-table-column>
            <el-table-column label="评分" prop="rating"></el-table-column>
            <el-table-column label="点击量" prop="click_number"></el-table-column>
            <el-table-column label="操作">
              <template #default="{ row }">
                <el-button v-if="!row.is_finished" type="primary" @click="goToUpdateChapter(row.id)">去更新</el-button>
                <el-button v-else type="primary" @click="Updateisfinished(row)">修改完结状态</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <div v-else>
          <p style="font-size: 20px; text-indent: 2em;">您还没有作品。</p>
        </div>
        <div style="margin-top: 20px;">
          <div style="text-align: center;">
            <el-button type="primary" style="background-color: green;font-size: 18px;"
              @click="goToWriteNewBook">去写新书</el-button>
          </div>
        </div>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';
import { ElMessageBox } from 'element-plus';

export default {
  name: "UserProfile",
  data() {
    return {
      user: null,
      loading: true,
    };
  },
  computed: {
    ...mapState(['token']),
  },
  mounted() {
    this.fetchMyInfo();
  },
  methods: {
    async fetchMyInfo() {
      try {
        const token = this.token;
        console.log('反馈5:', token);
        const response_user = await axios.get(`${this.$backend}/users/me`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.user = response_user.data;
        this.loading = false;
      } catch (error) {
        console.error('获取用户信息失败', error);
        this.loading = true;
      }
    },
    goToNovelPage(novel) {
      this.$router.push({ name: 'novelPage', params: { novelId: novel } });
    },
    goToUpdateChapter(novel) {
      this.$router.push({ name: 'updateChapterPage', params: { novelId: novel } });
    },
    goToWriteNewBook() {
      console.log('反馈3: goToWriteNewBook');
      this.$router.push('/writeNovel');
    },
    async confirmUpdate(row) {
      const confirmResult = await ElMessageBox.confirm('确定要修改完结状态吗？', '确认', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
      });
      if (confirmResult === 'confirm') {
        await this.Updateisfinished(row);
      }
    },
    async Updateisfinished(novel) {
      if (novel.is_visible) {
        try {
          const token = this.token;
          const response = await axios.patch(`${this.$backend}/novels/${novel.id}/finished/`, { novel }, {
            headers: {
              Authorization: `Bearer ${token}`
            }
          });
          // 更新本地数据状态
          const updatedNovelIndex = this.user.novels.findIndex(item => item.id === novel.id);
          if (updatedNovelIndex !== -1) {
            this.user.novels[updatedNovelIndex].is_finished = !this.user.novels[updatedNovelIndex].is_finished;
          }
          // 如果后端返回成功消息，将其显示在页面上
          this.message = response.data.detail || '完结状态更新成功';
        } catch (error) {
          // 如果后端返回错误信息，也将其显示在页面上
          this.message = error.response.data.detail || '完结状态更新失败';
          console.error('完结状态更新失败', error);
        }
      } else {
        await ElMessageBox.alert('小说已经被下架了，暂时无法更新。', '提示', {
          confirmButtonText: '确定'
        });
      }
    },
    onHover(row, hover) {
      row.isHovered = hover
    }
  }
};
</script>

<style>
.el-table th,
.el-table td {
  font-size: 18px;
}
</style>