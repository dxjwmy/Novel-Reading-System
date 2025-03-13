import axios from 'axios';
import { createRouter, createWebHistory } from 'vue-router';
import Home from './views/Home.vue';
import Login from './views/Login.vue';
import Register from './views/Register.vue';
import UserProfile from './views/UserProfile.vue'; 
import Administrator from './views/Administrator.vue'
import NovelPage from './views/NovelPage.vue';
import UpdateChapterPage from './views/UpdateChapterPage.vue';
import SearchResults from './views/SearchResults.vue';
import CreateNovel from './views/CreateNovel.vue';
import CategoryNovelPage from './views/CategoryPage.vue'
import rank from './views/Rank.vue'
import Wordcount from './views/WordCount.vue'
import Finish from './views/Finished.vue'
import Chapterreader from './views/ChapterRead.vue'
import Authorpage from './views/AuthorPage.vue'

const routes = [
  {path: '/',component: Home},
  {path: '/login',component: Login},
  {path: '/register',component: Register},
  {path: '/users/me',component: UserProfile},
  {path: '/Administrator',component: Administrator},
  {path: '/writeNovel',component: CreateNovel },
  {path: '/novels/:novelId', name: 'novelPage', component: NovelPage },
  {path: '/updateChapter/:novelId', name: 'updateChapterPage', component: UpdateChapterPage },
  {path: '/title/:searchKeyword', name: 'searchResults', component: SearchResults,},
  {path: '/category/:category', component: CategoryNovelPage},
  {path: '/rank', component: rank},
  {path: '/字数排序', component: Wordcount},
  {path: '/finish', component: Finish},
  {path: '/chapter/:novelId/:chapterId', component: Chapterreader},
  {path: '/author/:authorId', component: Authorpage},
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  document.body.style.backgroundColor = 'aliceblue';
  next();
});

export default router;