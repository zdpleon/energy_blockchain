<template>
    <div>
        <div class="breadcrumb-container">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>主面板</el-breadcrumb-item>
                <el-breadcrumb-item>用户充值</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <el-tabs type="border-card" style="width: 1000px" v-loading="loading" element-loading-text="正在充值">
            <el-tab-pane label="账户信息">
                <div class="account-body" >
                    <span class="account-title">用户名称</span>
                    <el-input class="btn" size="small" v-model="username" :disabled="true"></el-input>
                    <span class="account-title">账户余额</span>
                    <el-input class="btn" size="small" v-model="money" :disabled="true"></el-input>
                    <span class="account-title">用户充值</span>
                    <el-input class="btn" size="small" v-model="value"></el-input>
                    <el-button type="primary" size="small" @click="topUpUser" style="margin: auto;text-align: center">提交修改</el-button>
                </div>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
  import axios from  'axios';
  export default {
    data() {
      return {
        position: 'top',
        value: 0.0,
        loading: false,
      }
    },
    computed: {
      username() {
        return this.$store.state.userInfo.username;
      },
      money() {
        return this.$store.state.userInfo.money;
      }
    },
    methods: {
      topUpUser() {
        let url = this.$store.state.host + '/api/pushMoney';
        let info = {
          userName: this.$store.state.userInfo.username,
          addMoney: this.value,
        };
        this.loading = true
        axios. post(url, info).then(res => {
          if (res.data.status === 'success') {
            this.loading = false;
            this.value = 0;
            this.$message({
              type: 'success',
              message: '充值成功',
            });
            this.$store.commit('changeUserInfoMoney', res.data.money);
          } else {
            this.loading = false;
            this.$message({
              type: 'error',
              message: '充值失败',
            });
          }
        }, (reject => {
          this.$message({
            type: 'error',
            message: '请求失败',
          });
        }));
      }
    }

  };
</script>

<style>
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