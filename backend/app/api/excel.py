from fastapi import APIRouter, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
import pandas as pd
import io

router = APIRouter()

@router.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(status_code=400, detail="Only .xlsx files are allowed")
    
    try:
        content = await file.read()
        df = pd.read_excel(io.BytesIO(content))
        
        # 验证必填列
        required_columns = ['IP地址*', 'SSH密码*']
        for col in required_columns:
            if col not in df.columns:
                raise HTTPException(status_code=400, detail=f"Missing required column: {col}")
        
        # 转换数据
        hosts = []
        for _, row in df.iterrows():
            host = {
                "hostname": row.get('主机名(可选)', ""),
                "ip": row.get('IP地址*'),
                "port": int(row.get('SSH端口', 22)),
                "username": row.get('SSH用户', "root"),
                "password": row.get('SSH密码*'),
                "department": row.get('运维单位', ""),
                "operator": row.get('运维人员', ""),
                "description": row.get('描述', ""),
                "tags": row.get('标签(JSON)', "{}")
            }
            hosts.append(host)
        
        return JSONResponse(content={"message": "Excel uploaded successfully", "hosts": hosts})
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing Excel file: {str(e)}")
