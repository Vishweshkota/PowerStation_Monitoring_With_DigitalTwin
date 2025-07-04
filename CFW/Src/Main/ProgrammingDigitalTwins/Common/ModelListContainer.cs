﻿

using System.Collections.Generic;

/**
 * MIT License
 * 
 * Copyright (c) 2024 Andrew D. King
 * 
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 * 
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 * 
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */
namespace LabBenchStudios.Pdt.Common
{
    /// <summary>
    /// This class is a simple wrapper around a prediction engine's
    /// model list for ease of transport.
    /// </summary>
    public class ModelListContainer
    {
        private string uri = null;
        private List<string> modelList = null;

        // constructors

        /// <summary>
        /// 
        /// </summary>
        /// <param name="uri"></param>
        /// <param name="modelList"></param>
        public ModelListContainer(string uri, List<string> modelList)
        {
            this.uri = uri;
            this.modelList = modelList;
        }

        // public methods

        /// <summary>
        /// 
        /// </summary>
        /// <returns></returns>
        public string GetUri()
        {
            return uri;
        }

        /// <summary>
        /// 
        /// </summary>
        /// <returns></returns>
        public List<string> GetModelList()
        {
            return modelList;
        }

    }

}
