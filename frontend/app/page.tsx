"use client";
import { useState } from 'react';
import { Upload, Button, message } from 'antd';
import { UploadOutlined } from '@ant-design/icons';
import { UploadChangeParam, UploadFile } from 'antd/lib/upload';

export default function Home() {
  const [fileList, setFileList] = useState<UploadFile<any>[]>([]);

  const props = {
    name: 'file',
    multiple: true,
    action: (file: File) => process.env.NEXT_PUBLIC_UPLOAD_URL + "/upload/" + file.name,
    method: 'PUT' as const,
    headers: {
      'Content-Type': 'application/pdf',
    },
    onChange(info: UploadChangeParam) {
      let fileList: UploadFile<any>[] = [...info.fileList];

      /* Limit the list to last 5 files */
      fileList = fileList.slice(-5);

      /* Read from response and show file link */
      fileList = fileList.map(file => {
        if (file.response) {
          file.url = file.response.url;
        }
        return file;
      });

      setFileList(fileList);
    },
  };

  const handleDownload = async () => {
    try {
      const response = await fetch(process.env.NEXT_PUBLIC_DOWNLOAD_URL as string);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();

      if (Array.isArray(data)) {
        data.forEach((url) => {
          window.open(url);
          /* Reset the file list after download */
          setFileList([]);
        });
      } else {
        message.info(data);
      }

    } catch (error: any) {
      message.error(`An error occurred: ${error.message}`);
    }
  };

  return (
      <div className="min-h-screen bg-black flex flex-col items-center justify-center text-white px-4 sm:px-0">
        <h1 className="text-4xl font-bold mb-8 text-center">ExtractGen by Bhishman Desai</h1>
        <div className="w-full sm:w-auto">
          <Upload {...props} fileList={fileList} className="upload-list-inline">
            <Button icon={<UploadOutlined />} size="large" type="primary" style={{border: '2px dotted white', width: '100%'}}>Upload your PDF</Button>
          </Upload>
          {fileList.length > 0 && (
              <Button size="large" type="primary" className="mt-4" style={{ width: '100%', border: '1px solid white' }} onClick={handleDownload}>
                Download
              </Button>
          )}
        </div>
      </div>
  );
}
