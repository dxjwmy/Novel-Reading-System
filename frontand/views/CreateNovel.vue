<template>
    <div class="create-novel-container">
        <h2 style="text-align: center;">写本新小说吧</h2>
        <el-form :model="novelForm" label-width="100px">
            <el-form-item label="标题">
                <el-input v-model="novelForm.title" style="font-size: 16px;"></el-input>
            </el-form-item>
            <el-form-item label="小说简介">
                <el-input type="textarea" v-model="novelForm.summary" style="font-size: 16px;" rows="7"></el-input>
            </el-form-item>
            <el-form-item label="小说分类">
                <el-select v-model="novelForm.category" style="font-size: 16px; ">
                    <el-option label="玄幻" value="玄幻"></el-option>
                    <el-option label="仙侠" value="仙侠"></el-option>
                    <el-option label="都市" value="都市"></el-option>
                    <el-option label="科幻" value="科幻"></el-option>
                    <el-option label="历史" value="历史"></el-option>
                    <el-option label="异世界" value="异世界"></el-option>
                    <el-option label="轻小说" value="轻小说"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="createNovel">提交</el-button>
            </el-form-item>
        </el-form>
        <div v-if="message" style="color: green;">{{ message }}</div>
    </div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';
import { ElMessageBox } from 'element-plus';

export default {
    name: "CreateNovelPage",
    data() {
        return {
            novelForm: {
                title: '',
                summary: '',
                category: ''
            },
            message: ''
        };
    },
    computed: {
        ...mapState(['token'])
    },
    methods: {
        async createNovel() {
            try {
                const token = this.token;
                const jsonData = {
                    title: this.novelForm.title,
                    summary: this.novelForm.summary,
                    category: this.novelForm.category
                };
                const response = await axios.post(
                    `${this.$backend}/createnovel/`, // 替换为实际的后端创建小说接口路径
                    jsonData,
                    {
                        headers: {
                            Authorization: `Bearer ${token}`
                        }
                    }
                );
                console.log('小说创建成功', response.data);
                console.log('小说id', response.data.id);
                this.message = response.data.detail || '小说创建成功';
                // 可以根据需要进行页面跳转或其他操作，比如跳转到小说列表页面等
                ElMessageBox.confirm('新书已经创建好了，是否现在去写第一章？', '提示', {
                    confirmButtonText: '是',
                    cancelButtonText: '否',
                    type: 'info'
                })
                    .then(() => {
                        // 用户点击“是”，进行相应操作，比如跳转到写第一章的页面
                        this.$router.push({ name: 'updateChapterPage', params: { novelId: response.data.id } });
                    })
                    .catch(() => {
                        // 用户点击“否”，不进行任何操作
                    });
            } catch (error) {
                console.error('小说创建失败', error);
                this.message = error.response.data.detail || '小说创建失败';
                // 可以添加更详细的错误处理，比如根据错误状态码显示不同的提示信息给用户
            }
        }
    }
};
</script>

<style>
.create-novel-container {
    width: 50%;
    margin: 0 auto;
    /* 这行代码用于使容器在水平方向上居中 */
}
</style>