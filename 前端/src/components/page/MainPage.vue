<template>
    <div>
        <div class="breadcrumb-container">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>主面板</el-breadcrumb-item>
                <el-breadcrumb-item>主页</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <el-tabs type="border-card" class="trade-box" style="width: 1000px">
            <el-tab-pane label="我的挂单" class="trade-title">
                <el-button @click="requestOwnPendingOrderData" type="primary" style="float: right;margin-bottom: 10px"
                           size="small">刷新
                </el-button>
                <el-table :data="everyPageMyPendingOrderData" border class="realTimeDataTable">
                    <el-table-column prop="id" label="订单编号"></el-table-column>
                    <el-table-column prop="seller" label="出售者"></el-table-column>
                    <el-table-column prop="size" label="电量"></el-table-column>
                    <el-table-column prop="price" label="电价"></el-table-column>
                    <el-table-column prop="flag" label="挂单状态"></el-table-column>
                    <el-table-column prop="operation" fixed="right" label="操作">
                        <template scope="scope">
                            <el-button size="small" @click="deleteCurrentPendingOrder(scope.$index, scope.row)">删除
                            </el-button>
                        </template>
                    </el-table-column>
                </el-table>
                <el-pagination :small="true" :page-size="5" layout="total, prev, pager, next" :total="ownOrderTotal"
                               style="float: right;margin-top: 10px" :current-page="myOrderCurrentPage"
                               @current-change="changeMyOrderPage"></el-pagination>
            </el-tab-pane>
        </el-tabs>

        <el-tabs type="border-card" class="trade-box" style="width: 1000px">
            <el-tab-pane label="挂单" class="trade-title">
                <el-form :inline="true" :model="pendingOrderInfo">
                    <el-form-item label="电量" prop="size">
                        <el-input v-model="pendingOrderInfo.size" placeholder="0"></el-input>
                    </el-form-item>
                    <el-form-item label="电价">
                        <el-input v-model="pendingOrderInfo.price" placeholder="0.0"></el-input>
                    </el-form-item>
                    <el-form-item>
                        <el-button type="primary" @click="pendingOrder">挂单</el-button>
                    </el-form-item>
                </el-form>
            </el-tab-pane>
        </el-tabs>

        <el-tabs type="border-card" class="trade-box" style="width: 1000px" v-loading="loading"
                 element-loading-text="后台处理中">
            <el-tab-pane label="挂单记录" class="trade-title">
                <el-button @click="requestAllPendingOrderData" type="primary" style="float: right;margin-bottom: 10px"
                           size="small">刷新
                </el-button>

                <el-table :data="everyPageAllPendingOrderData" border class="realTimeDataTable">
                    <el-table-column prop="id" label="#"></el-table-column>
                    <el-table-column prop="seller" label="出售者"></el-table-column>
                    <el-table-column prop="size" label="电量"></el-table-column>
                    <el-table-column prop="price" label="电价"></el-table-column>
                    <el-table-column prop="operation" fixed="right" label="操作">
                        <template scope="scope">
                            <el-button size="small" @click="purchase(scope.$index, scope.row)">购买</el-button>
                        </template>
                    </el-table-column>
                </el-table>
                <el-pagination :small="true" :page-size="5" layout="total, prev, pager, next" :total="allOrderTotal"
                               style="float: right;margin-top: 10px" :current-page="allOrderCurrentPage"
                               @current-change="changeAllOrderPage"></el-pagination>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>
<script>
  import axios from 'axios';
  export default {
    data() {
      return {
        size: 0,
        price: 0.0,
        ownPendingOrderData: [],
        allPendingOrderData: [],
        ownOrderTotal: 1,
        allOrderTotal: 1,
        loading: false,
        myOrderCurrentPage: 1,
        allOrderCurrentPage: 1,
        pendingOrderInfo: {
          size: '',
          price: '',
        },
      }
    },
    computed: {
      everyPageMyPendingOrderData() {
        let begin_num = (this.myOrderCurrentPage - 1) * 5;
        let end_num = this.myOrderCurrentPage * 5;
        return this.ownPendingOrderData.slice(begin_num, end_num);
      },
      everyPageAllPendingOrderData() {
        console.log(this.allPendingOrderData.length);
        let begin_num = (this.allOrderCurrentPage - 1) * 5;
        let end_num = this.allOrderCurrentPage * 5;
        return this.allPendingOrderData.slice(begin_num, end_num);
      },
    },
    methods: {
      pendingOrder() {
        let url = this.$store.state.host + '/api/postSellInfo';
        let info = {
          userName: this.$store.state.userInfo.username,
          price: this.pendingOrderInfo.price,
          size: this.pendingOrderInfo.size,
        };
        axios.post(url, info).then(res => {
          this.requestOwnPendingOrderData();

          this.$message({
            type: 'success',
            message: '挂单成功',
          });

        });
      },
      requestOwnPendingOrderData() {
        let url = this.$store.state.host + '/api/getMySellingList';
        let info = {
          userName: this.$store.state.userInfo.username,
        };

        axios.post(url, info).then(res => {
          this.ownPendingOrderData = res.data.data;
          res.data.data.forEach(value => {
            switch (value.flag) {
              case 0:
                value.flag = '挂单未交易';
                break;
              case 1:
                value.flag = '交易进行中';
                break;
              default:
                value.flag = '挂单已交易'
                break;
            }
          });
          this.ownOrderTotal = res.data.data.length;
        });
      },
      requestAllPendingOrderData() {
        let url = this.$store.state.host + '/api/getAllSelling';
        let info = {
          userName: this.$store.state.userInfo.username,
        };

        axios.post(url, info).then(res => {
          this.allPendingOrderData = res.data.data;
          this.allOrderTotal = res.data.data.length;
        });
      },
      deleteCurrentPendingOrder(index, row) {

        let url = this.$store.state.host + '/api/deleteMySellInfo';
        let info = {
          sellId: row.id,
        };
        axios.post(url, info).then(res => {
          if (res.data.status === 'success') {
            this.ownPendingOrderData.splice(index, 1);
            this.$message({
              type: 'success',
              message: '删除成功',
            });
          } else {
            if (res.data.flag === 'selling') {
              this.$message({
                type: 'warning',
                message: '交易正在进行中，请稍后再试',
              });
              row.flag = '交易进行中';
            } else {
              row.flag = '挂单已交易';
              this.$message({
                type: 'error',
                message: '挂单已经被购买，删除失败',
              });
            }
          }
        });
      },
      purchase(index, row) {
        let payMoney = parseFloat(row.size) * parseFloat(row.price);
        if (this.$store.state.userInfo.money < payMoney) {
          this.$message({
            type: 'warning',
            message: "余额不足",
          });
          return;
        }
        let url = this.$store.state.host + '/api/buy';
        let info = {
          sellId: row.id,
          userName: this.$store.state.userInfo.username,
        };
        this.loading = true;
        axios.post(url, info).then(res => {
          this.loading = false;
          if (res.data.status === 'success') {
            this.$store.commit('changeUserInfoMoney', res.data.money);
            this.allPendingOrderData.splice(index, 1);
            this.$message({
              type: 'success',
              message: "购买成功",
            });
          } else {
            this.$message({
              type: 'error',
              message: "购买失败",
            });
          }
        });
      },
      changeMyOrderPage(currentPage) {
        this.myOrderCurrentPage = currentPage;
      },
      changeAllOrderPage(currentPage) {
        this.allOrderCurrentPage = currentPage;
      },
    },
    beforeMount() {
      this.requestOwnPendingOrderData();
      this.requestAllPendingOrderData();
    }
  }
</script>
<style>
    .trade-box {
        margin-bottom: 40px;
    }

    .trade-label {
        font-size: 15px;
        text-align: center;
        height: 36px;
        display: inline-block;
        margin: auto;
        padding-top: 7px;
    }

    .trade-title {
        border-color: #d1dbe5;
    }

    .cell {
        text-align: center;
    }

    .el-input__inner {
        border-radius: 0 !important;
        box-shadow: 0 0 2px #ccc;

    }


</style>