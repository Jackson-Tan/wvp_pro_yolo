﻿/*
 * Copyright (c) 2016 The ZLMediaKit project authors. All Rights Reserved.
 *
 * This file is part of ZLMediaKit(https://github.com/xia-chu/ZLMediaKit).
 *
 * Use of this source code is governed by MIT license that can be found in the
 * LICENSE file in the root of the source tree. All contributing project authors
 * may be found in the AUTHORS file in the root of the source tree.
 */

#include "Http/HttpClientImp.h"

using namespace toolkit;

namespace mediakit {

void HttpClientImp::onConnect(const SockException &ex) {
    if (!isHttps()) {
        //https 302跳转 http时，需要关闭ssl
        setDoNotUseSSL();
        HttpClient::onConnect(ex);
    } else {
        TcpClientWithSSL<HttpClient>::onConnect(ex);
    }
}

} /* namespace mediakit */
