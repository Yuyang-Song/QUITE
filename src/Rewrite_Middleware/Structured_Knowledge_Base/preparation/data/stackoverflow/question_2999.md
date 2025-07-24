# Why EF core can not translate the count?
[Link to question](https://stackoverflow.com/questions/61699916/why-ef-core-can-not-translate-the-count)
**Creation Date:** 1589040927
**Score:** 0
**Tags:** ef-core-3.0
## Question Body
<p>I want to query multiple aggregate values from the database with the fastest in EF core way, I have found this <a href="https://stackoverflow.com/questions/8894684/entity-framework-multiple-counts-with-a-single-query">Entity Framework multiple counts with a single query</a> and tried this </p>

<pre><code>        public Task&lt;VouchersUsageMetrics&gt; BuildVouchersUsageMetrics(
            IQueryable&lt;Voucher&gt; vouchers,
            VoucherSetting voucherSetting,
            CancellationToken cancellationToken)
        {
            var startOfToday = this.dateTimeProvider.GetStartOfDay(this.dateTimeProvider.Now);
            return vouchers
                .Select(it =&gt; SelectExpressions.GetVoucherStatus.Invoke(it, startOfToday))
                .GroupBy(
                    it =&gt; 1,
                    (groupId, groupItems) =&gt;
                        new VouchersUsageMetrics(
                            voucherSetting.TotalPrepaidCount,
                            voucherSetting.MaxAvailablePostpaidCount)
                        {
                            Expired = groupItems.Count(it =&gt; it == (long)VoucherStatusEnum.Expired),
                            Assigned = groupItems.Count(it =&gt; it == (long)VoucherStatusEnum.Assigned),
                            Requested = groupItems.Count(it =&gt; it == (long)VoucherStatusEnum.Requested),
                        })
                .FirstOrDefaultAsync(cancellationToken);
        }
</code></pre>

<p>However I am getting next error: </p>

<blockquote>
  <p>System.InvalidOperationException: The LINQ expression
  '(GroupByShaperExpression: KeySelector: (1), 
  ElementSelector:(ProjectionBindingExpression: EmptyProjectionMember) )
      .Count(it => (long)it == 21)' could not be translated. Either rewrite the query in a form that can be translated...</p>
</blockquote>

<p>I have tried </p>

<ol>
<li>to replace <code>SelectExpressions</code> with constant.</li>
<li>Have tried to remove first <code>Select</code></li>
<li>have tried to query the table instead of queryable, e.g. <code>this.context.Vouchers</code></li>
</ol>

<p>, but always have the same error. I have no idea, why :) Afraid if fail to make it is working, have to use SQL Virtual Views, but really don't like to support them. Or possibly will try dapper for this place.</p>

<p>PS. This how the queryable passed to the method is being built</p>

<pre><code>            this.context.Vouchers
                .AsNoTracking()
                .AsExpandableEFCore()
                .Where(it =&gt; it.AgencyID == 1);
</code></pre>

<p>PPS. EF Core 3.1.1 is used</p>

