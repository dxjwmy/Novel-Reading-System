<template>
  <div style="display:flex;align-items:center;">
    <h1 class="home-h1" @click="goToHomePage" style="color: #336699; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);">笔趣阁
    </h1>
    <div class="search-container" style="margin-left:20px;">
      <input v-model="searchKeyword" placeholder="试试搜索？" style="width: 300px; /* 增加宽度 */ margin-bottom: 10px;" />
      <button @click="searchNovels">搜索</button>
    </div>
  </div>
  <el-menu class="home-menu" :default-active="activeIndex" mode="horizontal" @select="handleSelect"
    style="background-color: #336699;">
    <el-menu-item style="color: white; font-weight: bold; font-size: large" index="1">全部作品</el-menu-item>>
    <el-menu-item style="color: white; font-weight: bold; font-size: large" index="2">玄幻</el-menu-item>
    <el-menu-item style="color: white; font-weight: bold; font-size: large" index="3">仙侠</el-menu-item>
    <el-menu-item style="color: white; font-weight: bold; font-size: large" index="4">都市</el-menu-item>
    <el-menu-item style="color: white; font-weight: bold; font-size: large" index="5">科幻</el-menu-item>>
    <el-menu-item style="color: white; font-weight: bold; font-size: large" index="6">历史</el-menu-item>
    <el-menu-item style="color: white; font-weight: bold; font-size: large" index="7">异世界</el-menu-item>
    <el-menu-item style="color: white; font-weight: bold; font-size: large" index="8">轻小说</el-menu-item>
    <el-menu-item style="color: white; font-weight: bold; font-size: large" index="9">排行榜</el-menu-item>
    <el-menu-item style="color: white; font-weight: bold; font-size: large" index="10">字数</el-menu-item>
    <el-menu-item style="color: white; font-weight: bold; font-size: large" index="11">完结</el-menu-item>
  </el-menu>
  <br></br>
  <div style="width: 100%; display: flex; justify-content: center;">
    <div class="novel-container-chapter" v-if="novel">
      <!-- 添加点击小说标题跳转小说页面的绑定 -->
      <h3 style="text-align: left">
        {{ novel.title }}
      </h3>
      <div class="meta-info" style="text-align: left;">
        <!-- 添加点击作者跳转到作者主页的绑定 添加点击类别跳转到按类别查找小说页面的绑定-->
        <p>
          <span @click="goToAuthorPage(novel.author_id)">{{ novel.author_name }}著</span> |
          <span @click="goToCategoryPage(novel.category)">{{ novel.category }}</span> | {{ novel.is_finished?
            '完结'
            : '连载' }}
        </p>
      </div>
      <p style="text-align: left; word-wrap: break-word; width: 50%;">
        {{ novel.summary }}
      </p>
      <div class="other-info" style="text-align: left;">
        <p>{{ novel.word_count }}字 | {{ novel.rating }}分 |最新章节：{{ novel.current_chapter}}</p>
      </div>
    </div>
  </div>
  <div style="width: 100%; display: flex; justify-content: center; align-items: center;">
    <div style="width: 50%;">
      <div v-if="novel.chapters" style="margin-top: 20px;">
        <h2>小说章节列表：</h2>
        <div class="chapter-list-container">
          <ul style="display: flex; flex-wrap: wrap;">
            <li v-for="(chapter, index) in novel.chapters" :key="chapter.id"
              style="width: 33.33%; padding: 10px 0; border-bottom: 1px solid #ddd" @click="goToChapterPage(chapter.id)">
              <span>{{ index + 1 }}. {{ chapter.chapter_name }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { useRoute } from 'vue-router';
import { mapState } from 'vuex';

export default {
  name: 'NovelPage',
  data() {
    return {
      novel: null,
      activeIndex: '1',
      searchKeyword: ''
    };
  },
  computed: {
  ...mapState(['token']),
  },
  async created() {
    await this.fetchNovel();
  },
  methods: {
    handleSelect(key, keyPath) {
      if (key === '1') this.$router.push(`/`);
      if (key === '2') this.$router.push(`/category/${"玄幻"}`);
      if (key === '3') this.$router.push(`/category/${"仙侠"}`);
      if (key === '4') this.$router.push(`/category/${"都市"}`);
      if (key === '5') this.$router.push(`/category/${"科幻"}`);
      if (key === '6') this.$router.push(`/category/${"历史"}`);
      if (key === '7') this.$router.push(`/category/${"异世界"}`);
      if (key === '8') this.$router.push(`/category/${"轻小说"}`);
      if (key === '9') this.$router.push(`/rank`);
      if (key === '10') this.$router.push(`/字数排序`);
      if (key === '11') this.$router.push(`/finish`);
    },
    async fetchNovel() {
      try {
        const route = useRoute();
        const novelId = route.params.novelId;
        const token = this.token;
        const res = await axios.get(`${this.$backend}/novels/by_id/${novelId}`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        const chaptersRes = await axios.get(`${this.$backend}/novels/${novelId}/menu/`, {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });
        res.data.chapters = chaptersRes.data;
        this.novel = res.data;

      } catch (error) {
        if (error.res && error.res.status === 404) {
          console.error('No novel found.');
        } else if (error.res && error.res.status === 400) {
          console.error('Forbidden.');
        } else {
          console.error('An error occurred while fetching the novel.', error);
        }
      }
    },
    goToHomePage() {
      // 根据你的路由配置进行跳转，假设主页的路由路径是 '/'
      console.log(`跳转到主页`);
      this.$router.push('/');
    },
    searchNovels() {
      console.log(`跳转到小说名字为 ${this.searchKeyword} 的页面`);
      this.$router.push(`/title/${this.searchKeyword}`);
    },
    // 跳转到作者主页的方法
    goToAuthorPage(authorId) {
      console.log(`跳转到作者 ${authorId} 的主页`);
      this.$router.push(`/author/${authorId}`);
    },
    // 跳转到按类别查找小说页面的方法
    goToCategoryPage(category) {
      // 在这里实现跳转到按类别查找小说页面的逻辑
      console.log(`跳转到类别为 ${category} 的小说页面`);
      this.$router.push(`/category/${category}`);
    },
    // 跳转到章节页面的方法
    goToChapterPage(chapter) {
      // 在这里实现跳转到章节页面的逻辑
      console.log(`跳转到小说 ${this.novel.id}，章节 ${chapter}`);
      this.$router.push(`/chapter/${this.novel.id}/${chapter}`);
    }
  },
};
</script>

<style scoped>
/* 添加一些样式美化页面 */
.home-h1 {
  font-size: 28px;
  font-weight: bold;
  color: #333;
}

.chapter-list-container {
  border: 3px solid #89a3f0;
  padding: 10px;
}

.novel-container-chapter {
  display: flex; 
  flex-direction: column; 
  position: relative; 
  left: 25%;
  width: 100%;
}

p {
  font-size: 16px;
  color: #666;
}

ul {
  list-style: none;
  padding: 0;
}

li span {
  display: block;
  font-size: 18px;
  color: #444;
}
</style>