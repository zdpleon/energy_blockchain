<template>
    <div>
        <div class="breadcrumb-container">
            <el-breadcrumb separator="/">
                <el-breadcrumb-item>主面板</el-breadcrumb-item>
                <el-breadcrumb-item>交易记录</el-breadcrumb-item>
            </el-breadcrumb>
        </div>
        <el-tabs type="border-card" style="width: 1000px">
            <el-button @click="requestAllTradeData" type="primary" style="float: right;margin-bottom: 10px"
                       size="small">刷新
            </el-button>
            <el-tab-pane label="交易总记录">
                <el-table :data="currentPageTradeData" border>
                    <el-table-column prop="id" label="订单编号"></el-table-column>
                    <el-table-column prop="seller" label="出售者"></el-table-column>
                    <el-table-column prop="buyer" label="购买者"></el-table-column>
                    <el-table-column prop="size" label="电量"></el-table-column>
                    <el-table-column prop="price" label="电价"></el-table-column>
                    <el-table-column prop="status" label="状态"></el-table-column>
                </el-table>
                <el-pagination :small="true" :page-size="10" layout="total, prev, pager, next" :total="allTradeTotal"
                               style="float: right;margin-top: 10px" :current-page="allTradeCurrentPage"
                               @current-change="changeAllTradePage"></el-pagination>
            </el-tab-pane>
            <el-tab-pane label="已经购买">
                <el-table :data="currentPagePurchasedData" border>
                    <el-table-column prop="id" label="订单编号"></el-table-column>
                    <el-table-column prop="size" label="电量"></el-table-column>
                    <el-table-column prop="price" label="电价"></el-table-column>
                    <el-table-column prop="seller" label="卖出者"></el-table-column>
                    <el-table-column prop="buyer" label="购买者"></el-table-column>
                </el-table>
                <el-pagination :small="true" :page-size="10" layout="total, prev, pager, next" :total="purchasedTotal"
                               style="float: right;margin-top: 10px" :current-page="purchasedCurrentPage"
                               @current-change="changePurchasedPage"></el-pagination>
            </el-tab-pane>
            <el-tab-pane label="已经卖出">
                <el-table :data="currentPageSoldData" border>
                    <el-table-column prop="id" label="订单编号"></el-table-column>
                    <el-table-column prop="size" label="电量"></el-table-column>
                    <el-table-column prop="price" label="电价"></el-table-column>
                    <el-table-column prop="purchaser" label="购买者"></el-table-column>
                    <el-table-column prop="buyer" label="购买者"></el-table-column>
                </el-table>
                <el-pagination :small="true" :page-size="10" layout="total, prev, pager, next" :total="soldTotal"
                               style="float: right;margin-top: 10px" :current-page="soldCurrentPage"
                               @current-change="changeSoldPage"></el-pagination>
            </el-tab-pane>
        </el-tabs>
    </div>
</template>

<script>
  import axios from 'axios';
  export default {
    data() {
      return {
        allTradeData: [],
        allTradeTotal: 1,
        purchasedTotal: 1,
        soldTotal:1,
        allTradeCurrentPage: 1,
        purchasedCurrentPage: 1,
        soldCurrentPage: 1,
      }
    },
    computed: {

      purchasedData() {
         let purchasedData = this.allTradeData.filter((value) => {
          return value.status === '已经买入';
        });
         this.purchasedTotal = purchasedData.length;
         return purchasedData;
      },
      soldData() {
        let soldData =  this.allTradeData.filter((value) => {
          return value.status === '已经卖出'
        });
        this.soldTotal = soldData.length;
        return soldData;
      },
      currentPagePurchasedData() {
        let begin_num = (this.purchasedCurrentPage - 1) * 10;
        let end_num = this.purchasedCurrentPage * 10;
        return this.purchasedData.slice(begin_num, end_num);
      },
      currentPageSoldData() {
        let begin_num = (this.soldCurrentPage - 1) * 10;
        let end_num = this.soldCurrentPage * 10;
        return this.soldData.slice(begin_num, end_num);
      },

      currentPageTradeData() {
        let begin_num = (this.allTradeCurrentPage - 1) * 10;
        let end_num = this.allTradeCurrentPage * 10;
        return this.allTradeData.slice(begin_num, end_num);
      }
    },
    methods: {
      requestAllTradeData() {
        let url = this.$store.state.host + '/api/getTransRecord'
        let info = {
          userName: this.$store.state.userInfo.username,
        }
        axios.post(url, info).then(res => {
          res.data.data.forEach((value, index) => {
            switch (value.status) {
              case 'on':
                value.status = '等待交易';
                break;
              case 'selling':
                if (this.$store.state.userInfo.username === value.seller) {
                  value.status = '正在卖出';
                } else {
                  value.status = '正在买入';
                }
                break;
              case 'selled':
                if (this.$store.state.userInfo.username === value.seller) {
                  value.status = '已经卖出';
                } else {
                  value.status = '已经买入';
                }
                break;
            }
          });
          this.allTradeData = res.data.data;
          this.allTradeTotal = this.allTradeData.length;
        });
      },
      changeAllTradePage(currentPage) {
        this.allTradeCurrentPage = currentPage;
      },
      changePurchasedPage(currentPage) {
        this.purchasedCurrentPage = currentPage;
      },
      changeSoldPage(currentPage) {
        this.soldCurrentPage = currentPage;
      },
    },
    beforeMount() {
      this.requestAllTradeData();
    }
  };
</script>

<style>
    .breadcrumb-container {

        margin: 10px 0;
        border: 1px solid #d1dbe5;
        padding: 10px;
        width: 1000px;
        background-color: white;
        box-shadow: 0 0 2px #ccc;
    }

</style>