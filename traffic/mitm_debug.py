def request(ctx, flow):
    print flow.request.headers['host']
    print flow.response