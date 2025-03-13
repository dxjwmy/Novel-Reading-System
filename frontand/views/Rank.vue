<template>
    <div id="home">
        <div v-if="isLoggedIn">
            <div style="display:flex;align-items:center;">
                <h1 class="novel-h1" @click="goToHomePage"
                    style="color: #336699; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);">笔趣阁</h1>
                <h2 style="margin-left: 10px;">排行榜</h2>
                <div class="search-container" style="margin-left:20px;">
                    <input v-model="searchKeyword" placeholder="试试搜索？"
                        style="width: 300px; /* 增加宽度 */ margin-bottom: 10px;" />
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
            <div class="novel-container" style="text-align: center; position: relative;">
                <div class="novel-row" v-for="index in Math.ceil(novels.length / 2)" :key="index">
                    <div class="novel-card left-card"
                        v-for="novel in novels.slice((index - 1) * 2, (index - 1) * 2 + 1)" :key="novel.id">
                        <div style="display: flex; flex-direction: column;">
                            <!-- 添加点击小说标题跳转小说页面的绑定 -->
                            <h3 style="text-align: left" @click="goToNovelPage(novel.id)">{{ novel.title }}</h3>
                            <div class="meta-info" style="text-align: left;">
                                <!-- 添加点击作者跳转到作者主页的绑定 -->
                                <p>
                                    <span @click="goToAuthorPage(novel.author_id)">{{ novel.author_name }}著</span> |
                                    <span @click="goToCategoryPage(novel.category)">{{ novel.category }}</span> | {{
                                        novel.is_finished ?
                                            '完结'
                                            : '连载' }}
                                </p>
                            </div>
                            <p style="text-align: left; line-height: 1.5;">{{ novel.truncatedSummary }}</p>
                            <div class="other-info" style="text-align: left;">
                                <!-- 添加点击类别跳转到按类别查找小说页面的绑定 -->
                                <p>
                                    {{ novel.word_count }}字 | {{ novel.rating }}分 |
                                    <span class="chapter-link" @click="goToChapterPage(novel.current_chapter)">{{
                                        novel.current_chapter
                                        }}</span>
                                </p>
                            </div>
                        </div>
                    </div>
                    <div class="novel-card right-card" v-for="novel in novels.slice((index - 1) * 2 + 1, index * 2)"
                        :key="novel.id">
                        <div style="display: flex; flex-direction: column;">
                            <h3 style="text-align: left" @click="goToNovelPage(novel.id)">{{ novel.title }}</h3>
                            <div class="meta-info" style="text-align: left;">
                                <p>
                                    <span @click="goToAuthorPage(novel.author_id)">{{ novel.author_name }}著</span> |
                                    <span @click="goToCategoryPage(novel.category)">{{ novel.category }}</span> | {{
                                        novel.is_finished ?
                                            '完结'
                                            : '连载' }}
                                </p>
                            </div>
                            <p style="text-align: left; line-height: 1.5;">{{ novel.truncatedSummary }}</p>
                            <div class="other-info" style="text-align: left;">
                                <p>
                                    {{ novel.word_count }}字 | {{ novel.rating }}分 |
                                    <span class="chapter-link" @click="goToChapterPage(novel.current_chapter)">{{
                                        novel.current_chapter
                                        }}</span>
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-else class="waitlogin">
            <h2>需要token</h2>
            <h2>您需要先进行登录!</h2>
        </div>
    </div>
</template>



<script>
import axios from 'axios';
import { ElTable } from 'element-plus';
import { mapState } from 'vuex';

export default {
    name: "rank",
    components: {
        ElTable
    },
    data() {
        return {
            novels: [],
            searchKeyword: '',
            activeIndex: '9',
        };
    },
    computed: {
        ...mapState(['token', 'isLoggedIn']),
    },
    mounted() {
        const token = this.token;
        axios.get(`${this.$backend}/novels/rating/`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        })
            .then(response => {
                this.novels = response.data.map(novel => {
                    if (novel.summary && novel.summary.length > 50) {
                        return {
                            ...novel,
                            truncatedSummary: novel.summary.slice(0, 50) + '...'
                        };
                    } else {
                        return {
                            ...novel,
                            truncatedSummary: novel.summary
                        };
                    }
                });
            })
            .catch(error => {
                console.error('Error fetching novels:', error);
            });
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

        goToHomePage() {
            console.log(`跳转到主页`);
            this.$router.push('/');
        },
        searchNovels() {
            console.log(`跳转到小说名字为 ${this.searchKeyword} 的页面`);
            this.$router.push(`/title/${this.searchKeyword}`);
        },
        // 跳转到小说页面的方法
        goToNovelPage(novelId) {
            console.log(`跳转到小说 id 为 ${novelId} 的页面`);
            this.$router.push({ name: 'novelPage', params: { novelId } });
        },
        // 跳转到作者主页的方法
        goToAuthorPage(authorID) {
            console.log(`跳转到作者 ${authorID} 的主页`);
            this.$router.push(`/author/${authorID}`);
        },
        // 跳转到按类别查找小说页面的方法
        goToCategoryPage(category) {
            console.log(`跳转到类别为 ${category} 的小说页面`);
            this.$router.push(`/category/${category}`);
        },
    }
};
</script>
