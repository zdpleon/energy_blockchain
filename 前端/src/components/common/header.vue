<template>
    <el-row class="header">
        <el-col :span="4" class="header-title">
            <span>能源互联网交易平台</span>
        </el-col>
        <el-col :span="4" :offset="15">
            <el-dropdown trigger="click" @command="handleCommand">
                <span class="el-dropdown-link" style="color: white">{{username}}<i class="el-icon-caret-bottom el-icon--right"></i></span>
                <el-dropdown-menu slot="dropdown">
                    <el-dropdown-item command="a"><a @click="backToLoginPage" style="font-size: 13px" >退出</a></el-dropdown-item>
                </el-dropdown-menu>
            </el-dropdown>
        </el-col>
    </el-row>
</template>

<script>
  export default {
    data() {
      return {
        activeIndex: '1',
      };
    },
    computed: {
      username() {
        return this.$store.state.userInfo.username;
      }
    },
    methods: {
      handleCommand(command) {

      },
      backToLoginPage() {
        this.$router.push('/');
      }
    }
  }
</script>
<style >
    .header {
        position: fixed;
        width: 100%;
        height: 60px;
        font-size: 22px;
        line-height: 70px;
        background-color: #1f2d3d;
        z-index: 1;
        color: white;
    }
    .header-title {
        display: inline-block;
        float: left;
        margin-left: 25px;


    }

    .header .title {
        color: white;
    }

    .header .title {
        text-align: center;
    }

    .header .menuBar {
        background-color: #1f2d3d
    }

    .el-dropdown-menu__item {
        text-align: center;
    }
</style>

