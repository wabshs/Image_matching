<template>
  <div class="container">
    <link rel="stylesheet">


    <!--    左边的部分-->
    <div class="left-container">
      <h3>您想比较的图——您可以选择手动上传</h3>
      <div>
        <el-upload list-type="picture-card" auto-upload="auto-upload" action="http://127.0.0.1:5000/upload"
                   :on-success="handleSuccess"
                   :on-error="handleError"
                   limit="1"
                   :file-list="fileList">
          <i class="el-icon-plus"></i>
        </el-upload>
        <br>
        <div>
          <h3>或者点此
            <el-button type="primary" @click="openCameraWindow"><i class="el-icon-camera"></i>拍 照</el-button>
          </h3>

        </div>
        <img :src="imgUrl" alt="图" v-if="leftImgExist===true" class="leftImg">
      </div>

      <!--      锦木千束-->
      <div class="sakana"></div>

      <!--    弹出框-->
      <el-dialog
          title="请拍摄"
          :visible.sync="dialogVisible"
          width="50%"
      >
        <!--        调用摄像头的区域-->
        <div class="camera">
          <!--          视频窗口-->
          <div class="video-container">
            <h1>实时摄像头画面</h1>
            <video ref="video" width="100%" height="400" autoplay></video>
          </div>

          <!--          照片显示区域-->
          <div class="photo-container">
            <h1>拍照预览图</h1>
            <br>
            <img :src="photo" v-if="photo" alt="拍摄的照片" height="400"/>
          </div>

        </div>

        <span slot="footer" class="dialog-footer">
          <el-button type="success" v-if="photo" @click="savePhoto"><i
              class="el-icon-folder-checked"></i>保 存</el-button>
          <el-button @click="beforeDestroy">取 消</el-button>
          <el-button type="warning" @click="takePhoto"><i class="el-icon-camera"></i>拍 摄</el-button>
        </span>
      </el-dialog>

    </div>

    <!--    右边的部分-->
    <div class="right-container">
      <h3>原图——您可以选择手动上传</h3>
      <div>
        <el-upload list-type="picture-card" auto-upload="auto-upload">
          <i class="el-icon-plus"></i>
        </el-upload>
        <br>
        <div>
          <h3>或者点此
            <el-button type="primary"><i class="el-icon-camera"></i>拍 照</el-button>
          </h3>

        </div>
        <img :src="imgUrl" alt="图" v-if="leftImgExist===true" class="leftImg">
      </div>
    </div>

  </div>
</template>

<script>
import 'sakana-widget/lib/index.css';
import SakanaWidget from 'sakana-widget';


export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data() {
    return {
      imgUrl: "",
      leftImgExist: false,
      rightImgExist: false,
      dialogVisible: false,
      photo: null,
      videoStream: null,
      fileList: [],
    }
  },

  mounted() {
    new SakanaWidget().mount('.sakana');
  },
  methods: {
    // 开启摄像头
    async startCamera() {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({video: true});
        const videoElement = this.$refs.video;
        videoElement.srcObject = stream;
      } catch (error) {
        console.error('Error accessing the camera:', error);
      }
    },
    // 回调函数
    handleSuccess(response) {
      // 上传成功处理逻辑
      this.$message.success('图片上传成功');
      console.log(response);
    },
    handleError(err) {
      // 上传失败处理逻辑
      this.$message.error('图片上传失败，请重试');
      console.error(err);
    },

    // 打开拍照窗口
    openCameraWindow() {
      this.dialogVisible = true
      this.startCamera()
    },
    // 拍摄照片
    takePhoto() {
      const videoElement = this.$refs.video;
      const canvas = document.createElement('canvas');
      canvas.width = videoElement.videoWidth;
      canvas.height = videoElement.videoHeight;
      const context = canvas.getContext('2d');
      context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
      this.photo = canvas.toDataURL('image/png');
    },

    //关闭窗口
    async beforeDestroy() {
      this.dialogVisible = false //关闭窗口
      await this.releaseCamera()
      window.location.reload()
    },

    // 释放资源
    releaseCamera() {
      if (this.videoStream) {
        this.videoStream.getTracks().forEach((track) => track.stop());
        this.videoStream = null;
        this.$refs.video.srcObject = null;

      }
    },
    savePhoto() {
      // 向后台发送照片数据
      fetch('http://127.0.0.1:5000/save-photo', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({photoDataUrl: this.photo}),
      }).then(response => response.json()).then(data => {
        console.log(data.message);
        // 成功提示
        // 关闭dialog
        this.dialogVisible = false
        this.$message.success('照片上传成功!');
        const photoDataUrl = this.photo; // 替换成实际的照片数据URL
        this.fileList.push({url: photoDataUrl});
      }).catch(error => {
        console.error(error);
        // 失败提示
        this.$message.error('照片上传失败!')
      });
    },
  }

}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>


.container {
  display: flex;
  height: 100vh;

}

.leftImg {
  max-width: 100%;
  height: auto;
  width: 100%;
}

.left-container,
.right-container {
  flex: 1;
  border: 1px solid #ccc;
}

.camera {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.video-container, .photo-container {
  width: 48%; /* 设置为48%以留出一定的间隔 */
  height: 400px;
  text-align: center;
}

.photo-container img {
  max-width: 100%; /* 让图片不超过父容器的宽度 */
  height: auto; /* 根据宽度自动调整高度，保持比例 */
}

</style>
