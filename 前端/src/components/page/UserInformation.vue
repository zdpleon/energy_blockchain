<template>
    <div>
        <div class="breadcrumb-container">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>账户</el-breadcrumb-item>
                <el-breadcrumb-item>用户信息</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <el-tabs type="border-card" style="width: 1000px">
            <el-tab-pane label="账户信息">
                <div class="account-body">
                    <span class="account-title">用户名称</span>
                    <el-input class="btn" size="small" v-model="username" :disabled="true"></el-input>
                    <span class="account-title">账户余额</span>
                    <el-input class="btn" size="small" v-model="money" :disabled="true"></el-input>
                </div>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
  export default {
    data() {
      return {

      }
    },
    computed: {
      username() {
        return this.$store.state.userInfo.username;
      },
      money() {
        return this.$store.state.userInfo.money;
      }
    }
  };
</script>

<style >
    .account-body {
        font-size: 14px;
        width: 300px;
    }
    .account-body .account-title {
    }
    .btn {
        margin-top: 10px;
        margin-bottom: 10px;

    }





</style>