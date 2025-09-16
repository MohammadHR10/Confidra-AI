'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { ShieldCheckIcon, DocumentArrowUpIcon, ClipboardDocumentIcon } from '@heroicons/react/24/outline'
import DocumentUpload from '../components/DocumentUpload'
import TextInput from '../components/TextInput'
import QuerySection from '../components/QuerySection'

export default function Home() {
  const [documentProcessed, setDocumentProcessed] = useState(false)
  const [documentName, setDocumentName] = useState('')
  const [processingStatus, setProcessingStatus] = useState<'idle' | 'processing' | 'success' | 'error'>('idle')

  const handleDocumentProcessed = (filename: string, success: boolean) => {
    if (success) {
      setDocumentProcessed(true)
      setDocumentName(filename)
      setProcessingStatus('success')
    } else {
      setProcessingStatus('error')
    }
  }

  return (
    <div className="min-h-screen bg-primary text-white">
      {/* Header */}
      <header className="flex items-center p-8">
        <div className="flex items-center space-x-4">
          <div className="w-8 h-8 bg-secondary rounded-full flex items-center justify-center">
            <ShieldCheckIcon className="w-5 h-5 text-primary" />
          </div>
          <h1 className="text-xl font-poppins font-medium text-secondary">
            Confidra AI
          </h1>
        </div>
      </header>

      {/* Hero Section */}
      <motion.div 
        className="text-center py-16 px-8"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <h1 className="text-4xl md:text-5xl font-poppins font-medium text-white mb-4">
          Scan your contract for NDA risks.
        </h1>
        <p className="text-sm text-gray-300 mb-6 font-inter">
          Your data is processed securely and never stored.
        </p>
        <p className="text-2xl text-white mb-12 font-inter max-w-2xl mx-auto">
          Upload a document or paste text below.<br />
          We'll scan it against your NDA and compliance rules
        </p>
      </motion.div>

      {/* Upload Section */}
      <div className="max-w-6xl mx-auto px-8 pb-16">
        <div className="grid md:grid-cols-2 gap-8">
          {/* Document Upload */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <div className="flex items-center space-x-2 mb-4">
              <DocumentArrowUpIcon className="w-6 h-6 text-white" />
              <h3 className="text-xl font-poppins font-medium">Upload Document</h3>
            </div>
            <DocumentUpload 
              onDocumentProcessed={handleDocumentProcessed}
              processingStatus={processingStatus}
              setProcessingStatus={setProcessingStatus}
            />
          </motion.div>

          {/* Text Input */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <div className="flex items-center space-x-2 mb-4">
              <ClipboardDocumentIcon className="w-6 h-6 text-white" />
              <h3 className="text-xl font-poppins font-medium">Paste Text</h3>
            </div>
            <TextInput 
              onTextProcessed={handleDocumentProcessed}
              processingStatus={processingStatus}
              setProcessingStatus={setProcessingStatus}
            />
          </motion.div>
        </div>
      </div>

      {/* Query Section */}
      {documentProcessed && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="border-t border-gray-600 pt-16"
        >
          <QuerySection documentName={documentName} />
        </motion.div>
      )}
    </div>
  )
}
