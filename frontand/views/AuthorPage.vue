<template>
    <div style="display:flex;align-items:center;">
        <h1 class="home-h1" @click="goToHomePage" style="color: #336699; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);">
            笔趣阁
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
    <div>
        <div style="margin-top: 10px;"> </div>
        <h2 style=" text-indent: 2em; ">作者信息</h2>
        <el-row v-if="loading">
            <el-col>
                <p>加载中...</p>
            </el-col>
        </el-row>
        <el-row v-else>
            <el-col>
                <p style="font-size: 20px; text-indent: 2em; float: left; width: 30%;">作者名：{{ user.username }}</p>
                <div style="margin-top: 100px;"> </div>
                <div v-if="Array.isArray(user.novels) && user.novels.length > 0">
                    <h2>作品列表：</h2>
                    <el-table :data="user.novels" style="width: 100%">
                        <el-table-column label="标题" prop="title">
                            <template #default="{ row }">
                                <a :style="{ fontSize: '18px', color: row.isHovered ? 'blue' : '' }"
                                    @mouseenter="onHover(row, true)" @mouseleave="onHover(row, false)"
                                    @click="goToNovelPage(row.id)">{{ row.title }}</a>
                            </template>
                        </el-table-column>
                        <el-table-column label="分类" prop="category"></el-table-column>
                        <el-table-column label="完结状态">
                            <template #default="{ row }">
                                <span :style="{ cursor: 'pointer' }">{{ row.is_finished ?
                                    '已完结' : '未完结'
                                    }}</span>
                            </template>
                        </el-table-column>
                        <el-table-column label="当前章节" prop="current_chapter"></el-table-column>
                        <el-table-column label="当前字数" prop="word_count"></el-table-column>
                        <el-table-column label="评分" prop="rating"></el-table-column>
                        <el-table-column label="点击量" prop="click_number"></el-table-column>
                    </el-table>
                </div>
                <div v-else>
                    <p style="font-size: 20px; text-indent: 2em;">没有作品。</p>
                </div>
            </el-col>
        </el-row>
    </div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';
import { useRoute } from 'vue-router';

export default {
    name: "Authorpage",
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
                const route = useRoute();
                const authorId = route.params.authorId;
                const token = this.token;
                console.log('反馈5:', token);
                const response_user = await axios.get(`${this.$backend}/userid/${authorId}`, {
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
        goToNovelPage(novel) {
            console.log('反馈：', novel);
            this.$router.push({ name: 'novelPage', params: { novelId: novel } });
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

.author-info-container {
    width: 70%;
    float: right;
}
</style>