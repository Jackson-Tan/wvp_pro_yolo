package com.genersoft.iot.vmp.gb28181.bean;

import java.time.Instant;
import java.util.List;

/**
 * @author lin
 */
public class CatalogData {
    /**
     * 命令序列号
     */
    private int sn;
    private int total;
    private List<DeviceChannel> channelList;
    private Instant lastTime;
    private Device device;
    private String errorMsg;

    public enum CatalogDataStatus{
        ready, runIng, end
    }
    private CatalogDataStatus status;


    public int getSn() {
        return sn;
    }

    public void setSn(int sn) {
        this.sn = sn;
    }

    public int getTotal() {
        return total;
    }

    public void setTotal(int total) {
        this.total = total;
    }

    public List<DeviceChannel> getChannelList() {
        return channelList;
    }

    public void setChannelList(List<DeviceChannel> channelList) {
        this.channelList = channelList;
    }

    public Instant getLastTime() {
        return lastTime;
    }

    public void setLastTime(Instant lastTime) {
        this.lastTime = lastTime;
    }

    public Device getDevice() {
        return device;
    }

    public void setDevice(Device device) {
        this.device = device;
    }

    public String getErrorMsg() {
        return errorMsg;
    }

    public void setErrorMsg(String errorMsg) {
        this.errorMsg = errorMsg;
    }

    public CatalogDataStatus getStatus() {
        return status;
    }

    public void setStatus(CatalogDataStatus status) {
        this.status = status;
    }
}
