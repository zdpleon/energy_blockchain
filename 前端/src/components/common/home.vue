<template>
	<div>
		<v-head></v-head>
		<v-sidebar></v-sidebar>
		<div class="content">
            <div class="item">
                <router-view></router-view>
            </div>
        </div>
	</div>
</template>

<script>
	import vHead from './header.vue'
    import vSidebar from './sidebar.vue'
    import '../../../static/css/main.css'


	export  default {
	    components: {
	        vHead,
		    vSidebar,
	    }
	}
</script>

<style>

	.content {
		background :none repeat scroll 0 0 #F1F2F7;
		position: relative;
		left: 250px;
		right: 0;
		top: 60px;
		width: calc(100% - 250px);
		/*
		height: calc(100% - 70px);
		*/
		padding: 10px 40px;
		box-sizing: border-box;
        z-index: 0;
	}

    .content .item {
        position: relative !important;
        top:20px;

    }


</style>


