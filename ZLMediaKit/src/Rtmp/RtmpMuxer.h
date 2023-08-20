﻿/*
 * Copyright (c) 2016 The ZLMediaKit project authors. All Rights Reserved.
 *
 * This file is part of ZLMediaKit(https://github.com/xia-chu/ZLMediaKit).
 *
 * Use of this source code is governed by MIT license that can be found in the
 * LICENSE file in the root of the source tree. All contributing project authors
 * may be found in the AUTHORS file in the root of the source tree.
 */

#ifndef ZLMEDIAKIT_RTMPMUXER_H
#define ZLMEDIAKIT_RTMPMUXER_H

#include "Rtmp/Rtmp.h"
#include "Extension/Frame.h"
#include "Common/MediaSink.h"
#include "RtmpCodec.h"

namespace mediakit{

class RtmpMuxer : public MediaSinkInterface {
public:
    using Ptr = std::shared_ptr<RtmpMuxer>;

    /**
     * 构造函数
     */
    RtmpMuxer(const TitleMeta::Ptr &title);
    ~RtmpMuxer() override = default;

    /**
     * 获取完整的SDP字符串
     * @return SDP字符串
     */
    const AMFValue &getMetadata() const ;

    /**
     * 获取rtmp环形缓存
     * @return
     */
    RtmpRing::RingType::Ptr getRtmpRing() const;

    /**
     * 添加ready状态的track
     */
    bool addTrack(const Track::Ptr & track) override;

    /**
     * 写入帧数据
     * @param frame 帧
     */
    bool inputFrame(const Frame::Ptr &frame) override;

    /**
     * 刷新输出所有frame缓存
     */
    void flush() override;

    /**
     * 重置所有track
     */
    void resetTracks() override ;

    /**
     * 生成config包
     */
     void makeConfigPacket();
private:
    RtmpRing::RingType::Ptr _rtmp_ring;
    AMFValue _metadata;
    RtmpCodec::Ptr _encoder[TrackMax];
};


} /* namespace mediakit */

#endif //ZLMEDIAKIT_RTMPMUXER_H
