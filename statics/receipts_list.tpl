<h1>Receipts List </h1>
<div>
    <a href="add-new-receipt">Add New Receipt</a>

</div>

<table>
    <thead>
    <tr>
        <th>Title</th>
        <th>Payer</th>
        <th>Date</th>
        <th>Status</th>
        <th>Amount</th>
    </tr>
    </thead>
    <tbody>
    % for rcp in receipts:
    <tr>
            <td class="title">{{rcp.title}}</td>
            <td class="payer_name">{{rcp.payer_name}}</td>
            <td class="date">{{rcp.creation_date_1}}</td>
            <td class="status">{{rcp.status}}</td>
            <td class="total_payment">{{rcp.total_payment}}</td>
    </tr>
    % end
    </tbody>

</table>
<p>    {{len(receipts)}} items found.</p>
%rebase store_logged_in_layout
