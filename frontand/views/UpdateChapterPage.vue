<template>
  <div class="update-chapter-container">
    <h2 style="text-align: center;">更新小说章节</h2>
    <el-form :model="chapterForm" label-width="100px">
      <el-form-item label="章节编号">
        <el-input v-model="chapterForm.chapter_number" style="font-size: 18px;"></el-input>
      </el-form-item>
      <el-form-item label="章节名称">
        <el-input v-model="chapterForm.chapter_name" style="font-size: 18px;"></el-input>
      </el-form-item>
      <el-form-item label="章节内容">
        <el-input type="textarea" v-model="chapterForm.content" rows="15" style="font-size: 18px;"></el-input>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="updateChapter">提交</el-button>
      </el-form-item>
    </el-form>
    <div v-if="message" style="color: green;">{{ message }}</div>
    <div v-if="currentChapterInfo" style="margin-top: 20px; text-align: left;">
      当前小说处于第 {{ currentChapterInfo.current_chapter }} 章。
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';
import { useRoute } from 'vue-router';
import { ElMessageBox } from 'element-plus';

export default {
  name: "UpdateChapterPage",
  data() {
    return {
      chapterForm: {
        chapter_number: null,
        chapter_name: '',
        content: ''
      },
      novelId: null,
      message: "",
      currentChapterInfo: null
    };
  },
  computed: {
   ...mapState(['token']),
  },
  setup() {
    const route = useRoute();
    return { route };
  },
  created() {
    // 从路由参数中获取小说 ID
    this.novelId = this.route.params.novelId;
    this.fetchCurrentChapter();
  },
  methods: {
    async fetchCurrentChapter() {
      try {
        const token = this.token;
        const res = await axios.get(`${this.$backend}/novels/by_id/${this.novelId}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        this.currentChapterInfo = res.data;
      } catch (error) {
        console.error('获取当前章节信息失败', error);
      }
    },
    async updateChapter() {
      try {
        const token = this.token;
        const jsonData = {
          chapter_name: this.chapterForm.chapter_name,
          chapter_content: this.chapterForm.content,
          chapter_number: this.chapterForm.chapter_number
        };
        const response = await axios.post(
          `${this.$backend}/novels/${this.novelId}/chapters_create/`,
          jsonData,
          {
            headers: {
              Authorization: `Bearer ${token}`
            }
          }
        );
        console.log('章节更新成功', response.data);
        this.message = response.data.detail || '章节更新成功';
        // 弹窗提醒
        ElMessageBox.confirm('章节更新成功！是否继续更新下一章？', '提示', {
          confirmButtonText: '是',
          cancelButtonText: '否'
        })
         .then(() => {
            // 用户点击“是”，继续更新下一章
            //this.$router.push({ name: 'updateChapterPage', params: { novelId: this.novelId } });
            location.reload();
          })
         .catch(() => {
            this.$router.push('/users/me');
          });
      } catch (error) {
        console.error('章节更新失败', error);
        this.message = error.response.data.detail || '章节更新失败';
        // 可以添加更详细的错误处理，比如根据错误状态码显示不同的提示信息给用户
      }
    }
  }
};
</script>

<style>
.update-chapter-container {
  width: 50%;
  margin: 0 auto;
  /* 这行代码用于使容器在水平方向上居中 */
}

/* 新增样式，将提示文本移动到最左侧 */
.update-chapter-container div[v-if="currentChapterInfo"] {
  text-align: left;
}
</style>