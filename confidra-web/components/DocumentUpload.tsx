'use client'

import { useState, useCallback } from 'react'
import { motion } from 'framer-motion'
import { uploadDocument } from '../lib/api'

interface DocumentUploadProps {
  onDocumentProcessed: (filename: string, success: boolean) => void
  processingStatus: 'idle' | 'processing' | 'success' | 'error'
  setProcessingStatus: (status: 'idle' | 'processing' | 'success' | 'error') => void
}

export default function DocumentUpload({ 
  onDocumentProcessed, 
  processingStatus, 
  setProcessingStatus 
}: DocumentUploadProps) {
  const [selectedFile, setSelectedFile] = useState<File | null>(null)
  const [dragActive, setDragActive] = useState(false)

  const handleFiles = (files: FileList | null) => {
    if (files && files[0]) {
      const file = files[0]
      const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain']
      
      if (allowedTypes.includes(file.type)) {
        setSelectedFile(file)
      } else {
        alert('Please upload a PDF, DOCX, or TXT file.')
      }
    }
  }

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true)
    } else if (e.type === 'dragleave') {
      setDragActive(false)
    }
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    e.stopPropagation()
    setDragActive(false)
    handleFiles(e.dataTransfer.files)
  }, [])

  const handleFileInput = (e: React.ChangeEvent<HTMLInputElement>) => {
    handleFiles(e.target.files)
  }

  const processDocument = async () => {
    if (!selectedFile) return

    setProcessingStatus('processing')

    try {
      await uploadDocument(selectedFile)
      
      setProcessingStatus('success')
      onDocumentProcessed(selectedFile.name, true)
    } catch (error: any) {
      console.error('Error processing document:', error)
      setProcessingStatus('error')
      onDocumentProcessed(selectedFile.name, false)
      
      // Show user-friendly error message
      alert(error.message || 'Failed to upload document. Please check if the backend is running.')
    }
  }

  return (
    <div className="space-y-4">
      {/* Upload Area */}
      <div
        className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
          dragActive 
            ? 'border-accent bg-accent/10' 
            : 'border-gray-400 bg-white hover:border-accent hover:bg-accent/5'
        }`}
        onDragEnter={handleDrag}
        onDragLeave={handleDrag}
        onDragOver={handleDrag}
        onDrop={handleDrop}
      >
        <input
          type="file"
          accept=".pdf,.docx,.txt"
          onChange={handleFileInput}
          className="hidden"
          id="file-upload"
        />
        <label
          htmlFor="file-upload"
          className="cursor-pointer block text-gray-600"
        >
          {selectedFile ? (
            <div className="space-y-2">
              <div className="text-green-600 font-medium">
                ✅ {selectedFile.name}
              </div>
              <div className="text-sm text-gray-500">
                Click to change file
              </div>
            </div>
          ) : (
            <div className="space-y-2">
              <div className="text-2xl">📁</div>
              <div className="font-medium">
                Drop your file here or click to browse
              </div>
              <div className="text-sm text-gray-500">
                Supports PDF, DOCX, and TXT files
              </div>
            </div>
          )}
        </label>
      </div>

      {/* Scan Button */}
      {selectedFile && (
        <motion.button
          onClick={processDocument}
          disabled={processingStatus === 'processing'}
          className="w-full btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          whileHover={{ scale: processingStatus !== 'processing' ? 1.02 : 1 }}
          whileTap={{ scale: processingStatus !== 'processing' ? 0.98 : 1 }}
        >
          {processingStatus === 'processing' ? (
            <span className="flex items-center justify-center space-x-2">
              <div className="animate-spin w-4 h-4 border-2 border-white border-t-transparent rounded-full"></div>
              <span>Processing...</span>
            </span>
          ) : (
            '🔍 SCAN FOR RISKS'
          )}
        </motion.button>
      )}

      {/* Status Messages */}
      {processingStatus === 'success' && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="status-approved"
        >
          ✅ Document processed successfully!
        </motion.div>
      )}

      {processingStatus === 'error' && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="status-blocked"
        >
          ❌ Failed to process document
        </motion.div>
      )}
    </div>
  )
}
