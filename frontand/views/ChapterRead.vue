<template>
    <div style="display:flex;align-items:center;">
        <h1 class="home-h1" @click="goToHomePage" style="color: #336699; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);">
            笔趣阁</h1>
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
    
    <div class="novel-container">
        <h1 class="novel-title" style="text-align: center;">{{ chapter.chapter_name }}</h1>
        <p class="novel-content"
            style="font-family: '楷体'; padding: 20px; line-height: 1.8; text-indent: 2em; font-size: 20px;">{{
                chapter.chapter_content }}</p>
        <div class="chapter-navigation" style="display: flex; justify-content: center; gap: 10px;">
            <button v-if="this.pre_chapterid" @click="prevChapter" class="prev-chapter-btn">上一章</button>
            <button @click="showCatalog" class="catalog-btn">目录</button>
            <button v-if="this.after_chapterid" @click="nextChapter" class="next-chapter-btn">下一章</button>
        </div>
        <div v-if="showCatalogModal" class="catalog-modal" @click.self="hideCatalog">
            <div style="width: 100%; display: flex; justify-content: center; align-items: center;">
                <div style="width: 50%; background-color: #f9f9f9;"> <!-- 给目录添加实色背景 -->
                    <div v-if="chaptersList" style="margin-top: 20px;">
                        <h2>小说章节列表：</h2>
                        <div class="chapter-list-container">
                            <ul style="display: flex; flex-wrap: wrap;">
                                <li v-for="(chapter, index) in chaptersList" :key="chapter.id"
                                    style="width: 33.33%; padding: 10px 0; border-bottom: 1px solid #ddd"
                                    @click="goToChapter(chapter.id)">
                                    <span>{{ index + 1 }}. {{ chapter.chapter_name }}</span>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <ul>
            <li v-for="(item, index) in chaptersList" :key="item.id" @click="goToChapter(item.id)">
                {{ item.title }}
            </li>
        </ul>

    </div>
</template>

<script>
import axios from 'axios';
import { useRoute } from 'vue-router';
import { mapState } from 'vuex';

export default {
    name: 'Chapterreader',
    data() {
        return {
            chapter: null,
            showCatalogModal: false,
            chaptersList: [],
            pre_chapterid: null,
            after_chapterid: null,
        };
    },
    computed: {
        ...mapState(['token']),
    },
    watch: {
        '$route.params': {
            async handler(newParams, oldParams) {
                await this.fetchNovel();
            },
            immediate: true,
        },
    },
    methods: {
        async fetchNovel() {
            try {
                const route = useRoute();
                const novelId = route.params.novelId;
                const chapterId = route.params.chapterId;
                const token = this.token;
                console.log(`章节 ${chapterId}`);
                const res = await axios.get(`${this.$backend}/chapters/${chapterId}`, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
                const pre = await axios.get(`${this.$backend}/chapter/pre/${chapterId}`, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
                const after = await axios.get(`${this.$backend}/chapter/after/${chapterId}`, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
                const chaptersRes = await axios.get(`${this.$backend}/novels/${novelId}/menu/`, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });
                this.chapter = res.data;
                this.chaptersList = chaptersRes.data;
                this.pre_chapterid = pre.data.id;
                this.after_chapterid = after.data.id;
                console.log(`章节 ${this.chapter.chapter_name}`);
                console.log(`上一章 ${this.pre_chapterid}`);
                console.log(`下一章 ${this.after_chapterid}`);
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

        goToHomePage() {
            // 根据你的路由配置进行跳转，假设主页的路由路径是 '/'
            console.log(`跳转到主页`);
            this.$router.push('/');
        },
        searchNovels() {
            console.log(`跳转到小说名字为 ${this.searchKeyword} 的页面`);
            this.$router.push(`/title/${this.searchKeyword}`);
        },
        prevChapter() {
            this.$router.push(`/chapter/${this.chapter.novel_id}/${this.pre_chapterid}`);
        },
        nextChapter() {
            // const nextChapterId = this.getNextChapterId();
            this.$router.push(`/chapter/${this.chapter.novel_id}/${this.after_chapterid}`);
        },
        showCatalog() {
            this.showCatalogModal = true;
        },
        hideCatalog(event) {
            if (event.target.classList.contains('catalog-modal')) {
                this.showCatalogModal = false;
            }
        },
        goToChapter(chapterId) {
            const route = useRoute();
            const novelId = route.params.novelId;
            console.log(`跳转到小说 ${novelId}，章节 ${chapterId}`);
            this.$router.push(`/chapter/${novelId}/${chapterId}`);
        },
    },
};
</script>

<style scoped>
.novel-container {
    border: 2px solid rgb(123, 181, 235);
    transform: translateX(-50px);

}

.novel-reader-container {
    width: 50%;
    padding: 20px;
}

.novel-title {
    font-size: 28px;
    color: #333;
    margin-bottom: 10px;
}

.chapter-navigation {
    display: flex;
    justify-content: center;
    gap: 10px;
}

.prev-chapter-btn,
.next-chapter-btn,
.catalog-btn {
    padding: 10px 20px;
}

.prev-chapter-btn {
    background-color: #888;
    color: #fff;
}

.next-chapter-btn {
    background-color: #4CAF50;
    color: #fff;
}

.catalog-btn {
    background-color: #007BFF;
    color: #fff;
}

.catalog-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
}

.catalog-modal div {
    background-color: #f9f9f9;
    /* 给目录添加实色背景 */
}

.catalog-modal ul {
    list-style: none;
    padding: 0;
    display: flex;
    flex-wrap: wrap;
}

.catalog-modal li {
    width: 48%;
    margin-right: 4%;
    margin-bottom: 10px;
    padding: 10px;
    cursor: pointer;
}

.close-modal-btn {
    padding: 10px 20px;
    background-color: #f44336;
    color: #fff;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.catalog-page-container {
    width: 50%;
    padding: 20px;
}

.catalog-page-container ul {
    list-style: none;
    padding: 0;
}

.catalog-page-container li {
    padding: 10px;
    cursor: pointer;
}
</style>