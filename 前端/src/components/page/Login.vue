<template>
    <div>
    <div class="login-box">
        <h1 style="text-align: center">能源互联网交易平台</h1>
        <el-form :model="loginInfo" :rules="loginRules" >
            <el-form-item prop="username" class="form-control">
                <el-input v-model="loginInfo.username" placeholder="用户名"></el-input>
            </el-form-item>
            <el-form-item prop="password" class="form-control" style="margin-bottom: 30px">
                <el-input v-model="loginInfo.password" placeholder="密码"  type="password"></el-input>
            </el-form-item>
            <div class="login-btn">
                <el-button type="primary" @click="submitLoginInfo">登录</el-button>
            </div>
            <a style="float: right;padding-top: 10px;font-size: 13px;color: #20a0ff;cursor: pointer" @click="showRegisterForm">用户注册</a>
        </el-form>
    </div>
        <el-dialog title="用户注册" v-model="visible" top="10%" size="tiny" >
            <div class="register-box">
                <el-form :model="registerInfo" :rules="registerRules"  label-position="top">
                    <el-form-item prop="username" class="form-control" label=" 用户名">
                        <el-input v-model="registerInfo.username"></el-input>
                    </el-form-item>
                    <el-form-item prop="hardwareId" class="form-control" label="电表号">
                        <el-input v-model="registerInfo.hardwareId"></el-input>
                    </el-form-item>
                    <el-form-item prop="email" class="form-control" label="邮箱">
                        <el-input v-model="registerInfo.email"></el-input>
                    </el-form-item>
                    <el-form-item prop="password" class="form-control" label="密码">
                        <el-input v-model="registerInfo.password" type="password"></el-input>
                    </el-form-item>
                    <div class="register-btn">
                        <el-button type="primary" @click="submitRegisterInfo" style="text-align: center;margin: 15px auto;width: 80%;position: relative;left: 10%">提交</el-button>
                    </div>
                </el-form>
            </div>
        </el-dialog>
    </div>
</template>

<script>
  import axios from 'axios';
  export default {
    data() {
      return {
        loginInfo: {
          username: '',
          password: '',
        },
        loginRules: {
          username: [
            {required: true, message: '请输入用户名', trigger: 'blur'},
          ],
          password: [
            {
              required: true, message: '请输入登录密码', trigger: 'blur'},
          ]
        },
        registerInfo: {
          username: '',
          hardwareId: '',
          email: '',
          password: '',
        },
        registerRules: {
          username: [
            { required: true, message: '必填字段', trigger: 'blur'},
          ],
          hardwareId: [
            { required: true, message: '必填字段', trigger: 'blur'},
          ],
          email: [
            { required: true, message: '必填字段', trigger: 'blur', type: 'email'},
          ],
          password: [
            { required: true, message: '必填字段', trigger: 'blur'},
          ],
        },
        visible: false,
        loading: false,
      }
    },
    methods: {
      submitLoginInfo() {
        let url = this.$store.state.host + '/api/login';
        let userLoginInfo = this.loginInfo;
        axios.post(url, userLoginInfo).then(res => {
          if (res.data.status === 'success') {
            let info = {
              username: this.loginInfo.username,
              money: res.data.data.money,
            };
            this.$store.commit('initUserInfo', info);
            this.$router.push('/home/mainPage');
          } else {
            this.$message(
              {
                type: 'error',
                message: '用户名或者密码错误',
              }
            );
          }
        });
      },
      showRegisterForm() {
        this.visible = true;
      },
      submitRegisterInfo() {
        let url = this.$store.state.host + '/api/register/addUsers';
        let userRegisterInfo = this.registerInfo;
        axios.post(url, userRegisterInfo).then(res => {
          if (res.data.status === 'success') {
            this.$message({
                type: 'success',
                message: '注册成功',
                duration: 3000,
              });
            setTimeout(() => {
              this.visible = false;
            }, 3500);
          } else {
            this.$message(
              {
                type: 'error',
                message: '注册失败',
              }
            )
          }
        });
      },
    }
  }
</script>

<style>

    body {
        background-color: #f1f2f7 !important;
    }

    .login-box {
        box-sizing: border-box;
        padding: 40px;

        box-shadow: 0 0 2px #ccc;
        border-radius: 10px ;
        max-width: 400px;
        margin: 10% auto;
        background-color: white;
        font-family: "Helvetica Neue",Helvetica,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","微软雅黑",Arial,sans-serif;
    }
    .form-control {

        width: 100%;
        margin: 20px auto 20px auto;
    }
    .login-btn{
        margin: 0 auto;
        text-align: center;
    }

    .login-btn button {
        width: 100%;
    }

    .register-box .form-control {
        width: 80%;
        margin: 20px auto;
    }

    .el-form-item__error {
        position: relative;
        text-align: right;
        font-size: 14px;
        padding-top: 10px;
        padding-bottom: 0px;
    }





</style>