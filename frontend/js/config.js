const getBaseUrl = () => {
    return window.location.origin;
};

const getWsUrl = () => {
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
    return `${protocol}//${window.location.host}`;
};

const CONFIG = {
    API_BASE_URL: getBaseUrl(),
    WS_BASE_URL: getWsUrl()
};
