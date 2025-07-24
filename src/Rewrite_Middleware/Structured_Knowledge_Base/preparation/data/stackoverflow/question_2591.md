# Phoenix Ecto - Variable in model method
[Link to question](https://stackoverflow.com/questions/41838563/phoenix-ecto-variable-in-model-method)
**Creation Date:** 1485290309
**Score:** 0
**Tags:** elixir, phoenix-framework, ecto
## Question Body
<p>I am using the Phoenix web framework (Elixir) to rewrite a python based API delivery service we have and am running into a small issue.</p>

<p>I am trying to create a basic model method where by when called you pass it a serial number, it queries the database via Ecto and returns the result. Looking through the documentation I should be able to use interpolation to define the variable in the query but I am still getting an error.</p>

<p><strong>lib/test_result.ex</strong> file</p>

<pre><code>defmodule Webservices.TestResult do
  use Ecto.Schema

      schema "test_result" do
            field :date_added, Ecto.DateTime
            field :serial, :string
            field :sequence_id, :integer
            field :last_completed_stage, :integer
            field :last_completed_sequence, :integer
            field :workorder, :string
            field :product, :string
            field :is_complete, :integer
            field :is_scrapped, :integer
            field :value_stream, :string
            field :promise_date, Ecto.Date
            field :fail_lock, :integer
            field :sequence_rev, :integer
            field :date_updated, Ecto.DateTime
            field :date, Ecto.Date
            field :time, Ecto.Time
            field :ptyp2, :string
            field :wo_qty, :integer
            field :is_active, :integer
            field :is_time_lock, :integer
            field :time_lock_timestamp, Ecto.DateTime
            field :scrap_reason, :string
            field :scrapped_by, :integer
      end
  end
</code></pre>

<p><strong>lib/test_result_detail.ex</strong> file</p>

<pre><code>defmodule Webservices.TestResultDetail do
  use Ecto.Schema, :model
  import Ecto.Query

  schema "test_result_detail" do
    field :status_id, :integer
    field :station_id, :integer
    field :stage_id, :integer
    field :operator_id, :integer
    field :failstep, :string
    field :shift, :integer
    field :sequence_rev, :integer
    field :date_added, Ecto.Date
    field :date_timestamp, Ecto.DateTime
    field :date_time, Ecto.Time
    field :stage_order, :integer
    field :serial_number, :string
    field :is_retest, :integer
    field :retest_reason, :string

    has_many :result_id, Webservices.TestResult
end


  def last_completed_test(serial) do
    from c in Webservices.TestResultDetail,
      join: t in TestResult, on: t.id == c.result_id,
      select: {t.serial, c.station_id, c.stage_id, c.operator_id, c.sequence_rev},
      where: t.serial == ^serial,
      order_by: [desc: c.id],
      limit: 1
  end

end
</code></pre>

<p><strong>My controller:</strong></p>

<pre><code>defmodule Webservices.OPTController do
    use Webservices.Web, :controller

    alias Webservices.Router
    import Webservices.Router.Helpers

    def last(conn, %{"serial" =&gt; serial}) do
        import Ecto.Query

        results = Webservices.TestResultDetail.last_completed_test(serial)
        render(conn, "last.json", results: results)

    end
end
</code></pre>

<p>I am getting the following compile error:</p>

<blockquote>
  <p>== Compilation error on file web/controllers/opt_controller.ex ==
  ** (Ecto.Query.CompileError) variable <code>serial</code> is not a valid query expression. Variables need to be explicitly interpolated in queries
  with ^
      expanding macro: Ecto.Query.where/3
      web/controllers/opt_controller.ex:12: Webservices.OPTController.index/2
      (elixir) expanding macro: Kernel.|>/2
      web/controllers/opt_controller.ex:13: Webservices.OPTController.index/2
      (elixir) lib/kernel/parallel_compiler.ex:117: anonymous fn/4 in Kernel.ParallelCompiler.spawn_compilers/1</p>
</blockquote>

## Answers
### Answer ID: 41838855
<p>You joined two tables and in your <code>t</code> table there's <code>:serial</code> field. In <code>c</code> there's <code>:serial_number</code>. Just apply this <code>where</code> clause on <code>t.serial == ^serial</code>.</p>

