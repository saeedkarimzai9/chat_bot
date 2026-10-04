const {app,BrowserWindow}=require("electron");
const path=require("path");
function createWindow(){
 const win=new BrowserWindow({
  width:1440,height:900,minWidth:1100,minHeight:700,
  backgroundColor:"#0d0d0f",
  webPreferences:{contextIsolation:true,nodeIntegration:false}
 });
 win.loadFile(path.join(__dirname,"index.html"));
}
app.whenReady().then(()=>{createWindow();app.on("activate",()=>{if(BrowserWindow.getAllWindows().length===0)createWindow()})});
app.on("window-all-closed",()=>{if(process.platform!=="darwin")app.quit()});
