<template>
    <div id="category-page">
        <div style="display:flex;align-items:center;">
            <h1 class="novel-h1" @click="goToHomePage"
                style="color: #336699; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);">笔趣阁</h1>
            <h2 style="margin-left: 10px;">当前类别：{{ categoryName }}</h2>
            <div class="search-container" style="margin-left:20px;">
                <input v-model="searchKeyword" placeholder="试试搜索？"
                    style="width: 300px; /* 增加宽度 */ margin-bottom: 10px;" />
                <button @click="searchNovels">搜索</button>
            </div>
        </div>
        <el-menu class="home-menu" mode="horizontal" @select="handleSelect" style="background-color: #336699;">
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
            <div class="novel-row" v-for="index in Math.ceil(categoryNovels.length / 2)" :key="index">
                <div class="novel-card left-card"
                    v-for="novel in categoryNovels.slice((index - 1) * 2, (index - 1) * 2 + 1)" :key="novel.id">
                    <div style="display: flex; flex-direction: column;">
                        <!-- 添加点击小说标题跳转小说页面的绑定 -->
                        <h3 style="text-align: left" @click="goToNovelPage(novel.id)">{{ novel.title }}</h3>
                        <div class="meta-info" style="text-align: left;">
                            <!-- 添加点击作者跳转到作者主页的绑定 -->
                            <p>
                                <span @click="goToAuthorPage(novel.author_id)">{{ novel.author_name }}著</span> |
                                <span @click="goToCategoryPage(novel.category)">{{ novel.category }}</span> | {{
                                    novel.is_finished ? '完结' : '连载' }}
                            </p>
                        </div>
                        <p style="text-align: left; line-height: 1.5;">{{ novel.truncatedSummary }}</p>
                        <div class="other-info" style="text-align: left;">
                            <!-- 添加点击类别跳转到按类别查找小说页面的绑定 -->
                            <p>{{ novel.word_count }}字 | {{ novel.rating }}分 |最新章节：{{ novel.current_chapter }}</p>
                        </div>
                    </div>
                </div>
                <div class="novel-card right-card" v-for="novel in categoryNovels.slice((index - 1) * 2 + 1, index * 2)"
                    :key="novel.id">
                    <div style="display: flex; flex-direction: column;">
                        <h3 style="text-align: left" @click="goToNovelPage(novel.id)">{{ novel.title }}</h3>
                        <div class="meta-info" style="text-align: left;">
                            <p>
                                <span @click="goToAuthorPage(novel.author_id)">{{ novel.author_name }}著</span> |
                                <span @click="goToCategoryPage(novel.category)">{{ novel.category }}</span> | {{
                                    novel.is_finished ? '完结' : '连载' }}
                            </p>
                        </div>
                        <p style="text-align: left; line-height: 1.5;">{{ novel.truncatedSummary }}</p>
                        <div class="other-info" style="text-align: left;">
                            <p>{{ novel.word_count }}字 | {{ novel.rating }}分 |最新章节：{{ novel.current_chapter }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { ElTable } from 'element-plus';
import { mapState } from 'vuex';

export default {
    name: "CategoryNovelPage",
    components: {
        ElTable
    },
    data() {
        return {
            categoryNovels: [],
            searchKeyword: '',
            categoryName: ''
        };
    },
    computed: {
        ...mapState(['token', 'isLoggedIn'])
    },
    mounted() {
        this.init();
    },
    watch: {
        '$route.params': {
            handler() {
                this.init();
            },
            immediate: true
        }
    },
    methods: {
        init() {
            // 从路由参数中获取类别名称
            const token = this.token;
            this.categoryName = this.$route.params.category;
            axios.get(`${this.$backend}/novels/by_category/${this.categoryName}`, {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            })
                .then(response => {
                    this.categoryNovels = response.data.map(novel => {
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
                    console.error('Error fetching novels by category:', error);
                });
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

<style>
.novel-h1 {
    display: inline-block;
    width: 200px;
    color: #333;
    font-size: 36px;
    margin-left: 250px;
    margin-top: 20px;
}

.search-container {
    position: relative;
    left: 15%;
    transform: translateX(-50%);
    padding: 10px;
    text-align: center;
    margin-top: 20px;
    margin-bottom: 0px;
}

.search-container input {
    background-color: white;
    /* 设置输入框为透明色 */
    border: 1px solid #ccc;
    /* 可以添加边框以便区分 */
    padding: 9px;
    width: 300px;
    height: inherit;
}

.search-container button {
    border: 1px solid #ccc;
    padding: 8px 0;
    width: 40px;
    height: inherit;
    background-color: #dee2e6;
    transition: background-color 0.3s ease;
}

.search-container button:hover {
    background-color: #c0c0c0;
}

.novel-h2 {
    /* 设置标题的样式 */
    position: relative;
    /* 改为相对定位 */
    width: 37%;
    text-align: center;
    margin: 5px auto;
}

.novel-container {
    max-width: 900px;
    margin: 0 auto;
    position: relative;
    /* 改为相对定位 */
    left: 3%;
    transform: translateX(10px);
}

.novel-row {
    display: flex;
    flex-wrap: wrap;
}

.left-card,
.right-card {
    width: 45%;
    /* 增加卡片宽度 */
    padding: 5px;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15);
    background-color: #f5f5f5;
    margin-bottom: 15px;
    /* 减小卡片之间的垂直间距 */
    border-radius: 10px;
    margin-right: 20px;
}

.left-card {
    margin-left: 0px;
}

.left-card p,
.right-card p {
    line-height: 0.8;
    /* 减小行距，可根据实际效果调整数值 */
}

.left-card:hover,
.right-card:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.meta-info {
    font-size: 14px;
    color: #666;
}

.home-menu {
    display: flex;
    justify-content: center;
    margin-top: 5px;
    margin-bottom: 20px;
}

.home-menu.el-menu-item {
    text-align: center;
    margin: 0 100px;
    /* 增加菜单项之间的间距 */
    color: white;
    font-weight: bold;
}
</style>