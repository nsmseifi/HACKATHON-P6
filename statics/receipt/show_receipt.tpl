<!doctype html>
<html>
<head>
    <meta charset="utf-8">
    <title>{{rcp.get("title","")}}</title>

    <style>
    .invoice-box {
        max-width: 800px;
        margin: auto;
        padding: 30px;
        border: 1px solid #eee;
        box-shadow: 0 0 10px rgba(0, 0, 0, .15);
        font-size: 16px;
        line-height: 24px;
        font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
        color: #555;
    }

    .invoice-box table {
        width: 100%;
        line-height: inherit;
        text-align: left;
    }

    .invoice-box table td {
        padding: 5px;
        vertical-align: top;
    }

    .invoice-box table tr td:nth-child(2) {
        text-align: right;
    }

    .invoice-box table tr.top table td {
        padding-bottom: 20px;
    }

    .invoice-box table tr.top table td.title {
        font-size: 45px;
        line-height: 45px;
        color: #333;
    }

    .invoice-box table tr.information table td {
        padding-bottom: 40px;
    }

    .invoice-box table tr.heading td {
        background: #eee;
        border-bottom: 1px solid #ddd;
        font-weight: bold;
    }

    .invoice-box table tr.details td {
        padding-bottom: 20px;
    }

    .invoice-box table tr.item td{
        border-bottom: 1px solid #eee;
    }

    .invoice-box table tr.item.last td {
        border-bottom: none;
    }

    .invoice-box table tr.total td:nth-child(2) {
        border-top: 2px solid #eee;
        font-weight: bold;
    }

    @media only screen and (max-width: 600px) {
        .invoice-box table tr.top table td {
            width: 100%;
            display: block;
            text-align: center;
        }

        .invoice-box table tr.information table td {
            width: 100%;
            display: block;
            text-align: center;
        }
    }

    /** RTL **/
    .rtl {
        direction: rtl;
        font-family: Tahoma, 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
    }

    .rtl table {
        text-align: right;
    }

    .rtl table tr td:nth-child(2) {
        text-align: left;
    }
    </style>
</head>

<body>
    <div class="invoice-box">
        <table cellpadding="0" cellspacing="0">
            <tr class="top">
                <td colspan="2">
                    <table>
                        <tr>
                            <td class="title">
                              <img src="/statics/images/logo.png" style="width:100%; max-width:100px;">
                            </td>

                            <td>
                                Receipt #: {{str(rcp["id"])[:7].upper()}}<br>
                                Created: {{rcp["creation_date_1"]}}<br>
                                Due: {{rcp["creation_date_1"]}}
                            </td>
                        </tr>
                    </table>
                </td>
            </tr>

            <tr class="information">
                <td colspan="2">
                    <table>
                        <tr>
                            <td>
                                {{rcp["store"].get("full_name")}}<br>
                                {{rcp["store"].get("address")}}
                            </td>
                            %if user:
                            <td>

                                {{user.person_1.get("full_name")}}<br>
                                {{user.person_1.get("email")}}<br>
                                {{user.person_1.get("address")}}
                            </td>

                            %end
                            %if user is None:
                            <td></td>
                            %end
                        </tr>
                    </table>
                </td>
            </tr>


            <tr class="heading">
                <td>
                    Item
                </td>
                <td>Qty</td>
                <td>
                    Price
                </td>
            </tr>
     % for item in rcp.get("body"):
                        <tr class="item">
                            <td>{{item["name"]}}</td>
                            <td>{{item["qty"]}}</td>
                            <td>{{item["price"]}}</td>
                        </tr>
                        %end
            <tr>
                <td></td><td></td><td></td>
            </tr>
             <tr>
                <td></td><td></td><td></td>
            </tr>
             <tr>
                <td></td><td></td><td></td>
            </tr>
            <tr >
                <td></td>
                <td>SubTotal:</td>
                                <td>$ {{rcp["subtotal"]}}</td>

            </tr>
            <tr >
                <td></td>
                <td>HST:</td>
                <td>$ {{rcp["hst"]}}</td>

            </tr>

            <tr class="total">
                <td></td>
<td>Total:</td>
                <td>
                  $ {{rcp["total_payment"]}}
                </td>
            </tr>
        </table>
    %if user:

        <form>

            <button type="submit">Pay By My Account</button>
            <button type="submit">Pay By Paypal</button>
        </form>
    %end
    %if user is None:
     <form>
             <button type="submit">Login</button>
            <button type="submit">Pay By Paypal</button>
        </form>
    %end

    </div>
<div>
</div>
</body>
</html>
