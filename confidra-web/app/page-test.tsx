'use client'

import { useState } from 'react'
import { motion } from 'framer-motion'
import { ShieldCheckIcon, DocumentArrowUpIcon, ClipboardDocumentIcon } from '@heroicons/react/24/outline'

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
          {/* Document Upload Placeholder */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <div className="flex items-center space-x-2 mb-4">
              <DocumentArrowUpIcon className="w-6 h-6 text-white" />
              <h3 className="text-xl font-poppins font-medium">Upload Document</h3>
            </div>
            <div className="bg-card p-6 rounded-lg">
              <p className="text-gray-300">Document upload component will go here</p>
              <button 
                onClick={() => handleDocumentProcessed('test-doc.pdf', true)}
                className="mt-4 bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded"
              >
                Test Upload
              </button>
            </div>
          </motion.div>

          {/* Text Input Placeholder */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
          >
            <div className="flex items-center space-x-2 mb-4">
              <ClipboardDocumentIcon className="w-6 h-6 text-white" />
              <h3 className="text-xl font-poppins font-medium">Paste Text</h3>
            </div>
            <div className="bg-card p-6 rounded-lg">
              <p className="text-gray-300">Text input component will go here</p>
              <button 
                onClick={() => handleDocumentProcessed('pasted-text.txt', true)}
                className="mt-4 bg-green-600 hover:bg-green-700 px-4 py-2 rounded"
              >
                Test Text Input
              </button>
            </div>
          </motion.div>
        </div>
      </div>

      {/* Query Section Placeholder */}
      {documentProcessed && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="border-t border-gray-600 pt-16"
        >
          <div className="max-w-4xl mx-auto px-8">
            <h2 className="text-2xl font-poppins font-medium text-white mb-6 text-center">
              Ask questions about: {documentName}
            </h2>
            <div className="bg-card p-6 rounded-lg">
              <p className="text-gray-300 mb-4">Query section will go here</p>
              <div className="flex space-x-4">
                <input 
                  type="text" 
                  placeholder="Ask a question about your contract..."
                  className="flex-1 bg-primary border border-gray-600 rounded-lg px-4 py-2 text-white"
                />
                <button className="bg-accent hover:bg-purple-700 px-6 py-2 rounded-lg">
                  Ask
                </button>
              </div>
            </div>
          </div>
        </motion.div>
      )}
    </div>
  )
}
