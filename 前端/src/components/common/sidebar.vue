<template>
	<div class="sidebar">
		<el-menu  default-active="0" theme="dark" class="el-menu-vertical-demo" :unique-opened="true" router>
			<el-submenu index="0">
            <template slot="title"><i class="el-icon-menu"> 主界面</i> </template>
				<el-menu-item index="/home/mainPage">主页</el-menu-item>
				<el-menu-item index="/home/tradeRecord">交易记录</el-menu-item>
				<el-menu-item index="/home/topUpUser">用户充值</el-menu-item>
			</el-submenu>
     		<el-submenu index="1">
				<template slot="title"><i class="el-icon-setting"> 账户</i> </template>
				<el-menu-item index="/home/userInfo">用户信息</el-menu-item>
			</el-submenu>
		</el-menu>
	</div>
</template>

<script>
	export default {

	}
</script>

<style>
	.sidebar {
		display: block;
		position: fixed;
		width: 250px;
		height: calc(100% - 60px);
		left: 0;
		top: 60px;
		bottom: 0;
		background: #324057;
		z-index: 2;
	}

    /*
	.sidebar > ul {
		height: 100%;
	}
	*/
</style>